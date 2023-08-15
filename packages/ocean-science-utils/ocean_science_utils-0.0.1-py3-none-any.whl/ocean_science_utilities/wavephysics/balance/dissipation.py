import numba  # type: ignore
import numpy as np
import xarray

from typing import Callable, Dict, Tuple, Mapping

from ocean_science_utilities.wavephysics.balance.source_term import SourceTerm
from ocean_science_utilities.wavephysics.balance._numba_settings import (
    numba_nocache_parallel,
    numba_default,
)
from ocean_science_utilities.wavespectra.spectrum import FrequencyDirectionSpectrum
from ocean_science_utilities.wavespectra.operations import numba_integrate_spectral_data
from ocean_science_utilities.wavetheory.lineardispersion import (
    inverse_intrinsic_dispersion_relation,
)


class Dissipation(SourceTerm):
    name = "Dissipation"

    def __init__(self, parameters):
        super(Dissipation, self).__init__(parameters)
        self._dissipation_function = None

    def update_parameters(self, parameters: Mapping):
        for key in parameters:
            if key in self._parameters:
                self._parameters[key] = parameters[key]

    def rate(self, spectrum: FrequencyDirectionSpectrum) -> xarray.DataArray:
        data = _dissipation(
            spectrum.variance_density.values,
            spectrum.depth.values,
            self._dissipation_function,
            self.spectral_grid(spectrum),
            self.parameters,
        )
        return xarray.DataArray(data=data, coords=spectrum.coords(), dims=spectrum.dims)

    def bulk_rate(self, spectrum: FrequencyDirectionSpectrum) -> xarray.DataArray:
        data = _bulk_dissipation(
            spectrum.variance_density.values,
            spectrum.depth.values,
            self._dissipation_function,
            self.spectral_grid(spectrum),
            self.parameters,
        )
        return xarray.DataArray(
            data=data, coords=spectrum.coords_space_time, dims=spectrum.dims_space_time
        )

    def mean_direction_degrees(self, spectrum: FrequencyDirectionSpectrum):
        data, _ = _bulk_dissipation_direction(
            spectrum.variance_density.values,
            spectrum.depth.values,
            self._dissipation_function,
            self.spectral_grid(spectrum),
            self.parameters,
        )
        return xarray.DataArray(
            data=data, coords=spectrum.coords_space_time, dims=spectrum.dims_space_time
        )


@numba.jit(**numba_nocache_parallel)
def _dissipation(
    variance_density: xarray.DataArray,
    depth: xarray.DataArray,
    dissipation_source_term_function: Callable,
    spectral_grid: Dict[str, np.ndarray],
    parameters: Mapping,
) -> np.typing.NDArray:
    (
        number_of_points,
        number_of_frequencies,
        number_of_directions,
    ) = variance_density.shape

    dissipation = np.empty(
        (number_of_points, number_of_frequencies, number_of_directions)
    )
    for point_index in numba.prange(number_of_points):
        diss = dissipation_source_term_function(
            variance_density[point_index, :, :],
            depth[point_index],
            spectral_grid,
            parameters,
        )
        dissipation[point_index, :, :] = diss
    return dissipation


@numba.jit(**numba_nocache_parallel)
def _bulk_dissipation(
    variance_density: xarray.DataArray,
    depth: xarray.DataArray,
    dissipation_source_term_function: Callable,
    spectral_grid: Dict[str, np.ndarray],
    parameters: Mapping,
) -> np.typing.NDArray:
    number_of_points = variance_density.shape[0]
    dissipation = np.empty((number_of_points))

    for point_index in numba.prange(number_of_points):
        diss = dissipation_source_term_function(
            variance_density=variance_density[point_index, :, :],
            depth=depth[point_index],
            spectral_grid=spectral_grid,
            parameters=parameters,
        )
        dissipation[point_index] = numba_integrate_spectral_data(diss, spectral_grid)
    return dissipation


@numba.jit(**numba_nocache_parallel)
def _bulk_dissipation_direction(
    variance_density: xarray.DataArray,
    depth: xarray.DataArray,
    dissipation_source_term_function: Callable,
    spectral_grid: Dict[str, np.ndarray],
    parameters: Mapping,
) -> Tuple[np.typing.NDArray, np.typing.NDArray]:
    number_of_points = variance_density.shape[0]
    direction = np.empty((number_of_points))
    bulk = np.empty((number_of_points))

    for point_index in numba.prange(number_of_points):
        direction[point_index], bulk[point_index] = _bulk_dissipation_direction_point(
            variance_density[point_index, :, :],
            depth[point_index],
            dissipation_source_term_function,
            spectral_grid,
            parameters,
        )

    return direction, bulk


@numba.jit(**numba_default)
def _bulk_dissipation_direction_point(
    variance_density: xarray.DataArray,
    depth: xarray.DataArray,
    dissipation_source_term_function: Callable,
    spectral_grid: Dict[str, np.ndarray],
    parameters: Mapping,
) -> Tuple[float, float]:
    number_of_frequency = variance_density.shape[0]
    number_of_direction = variance_density.shape[1]

    dissipation = dissipation_source_term_function(
        variance_density=variance_density,
        depth=depth,
        spectral_grid=spectral_grid,
        parameters=parameters,
    )

    bulk = numba_integrate_spectral_data(dissipation, spectral_grid)
    radian_frequency = spectral_grid["radian_frequency"]
    radian_direction = spectral_grid["radian_direction"]
    frequency_step = spectral_grid["frequency_step"]
    direction_step = spectral_grid["direction_step"]
    wave_number = inverse_intrinsic_dispersion_relation(radian_frequency, depth)
    cosine = np.cos(radian_direction)
    sine = np.sin(radian_direction)

    kx = 0.0
    ky = 0.0

    # Disspation weighted average wave number to guestimate the wind direction.
    # Note dissipation is negative- hence the minus signs.
    for frequency_index in range(number_of_frequency):
        for direction_index in range(number_of_direction):
            kx -= (
                wave_number[frequency_index]
                * cosine[direction_index]
                * dissipation[frequency_index, direction_index]
                * frequency_step[frequency_index]
                * direction_step[direction_index]
            )

            ky -= (
                wave_number[frequency_index]
                * sine[direction_index]
                * dissipation[frequency_index, direction_index]
                * frequency_step[frequency_index]
                * direction_step[direction_index]
            )

    return (np.arctan2(ky, kx) * 180 / np.pi) % 360.0, bulk
