import numba  # type: ignore
import numpy as np
import xarray

from typing import Callable, Dict, Literal, Mapping, Optional, Tuple


from ocean_science_utilities.wavephysics.balance._numba_settings import (
    numba_default,
    numba_nocache_parallel,
)
from ocean_science_utilities.wavephysics.balance.source_term import SourceTerm
from ocean_science_utilities.wavephysics.balance.stress import (
    _roughness_estimate,
    _wave_supported_stress,
    _tail_supported_stress,
)
from ocean_science_utilities.wavespectra.operations import numba_integrate_spectral_data
from ocean_science_utilities.wavespectra.spectrum import FrequencyDirectionSpectrum

TWindInputType = Literal["u10", "friction_velocity", "ustar"]


class WindGeneration(SourceTerm):
    name = "base"

    def __init__(self, parmaters):
        super(WindGeneration, self).__init__(parmaters)
        self._wind_source_term_function = None
        self._tail_stress_parametrization_function = _tail_stress_parametrization_none

    def update_parameters(self, parameters: Mapping):
        for key in parameters:
            if key in self._parameters:
                self._parameters[key] = parameters[key]

    def rate(
        self,
        spectrum: FrequencyDirectionSpectrum,
        speed: xarray.DataArray,
        direction: xarray.DataArray,
        roughness_length: Optional[xarray.DataArray] = None,
        wind_speed_input_type: TWindInputType = "u10",
        **kwargs,
    ) -> xarray.DataArray:
        if roughness_length is None:
            roughness_length = self.roughness(
                speed, direction, spectrum, wind_speed_input_type=wind_speed_input_type
            )

        wind = (speed.values, direction.values, wind_speed_input_type)
        wind_input = _wind_generation(
            spectrum.variance_density.values,
            wind=wind,
            depth=spectrum.depth.values,
            roughness_length=roughness_length.values,
            wind_source_term_function=self._wind_source_term_function,
            spectral_grid=self.spectral_grid(spectrum),
            parameters=self.parameters,
        )
        return xarray.DataArray(
            data=wind_input, dims=spectrum.dims, coords=spectrum.coords()
        )

    def bulk_rate(
        self,
        spectrum: FrequencyDirectionSpectrum,
        speed: xarray.DataArray,
        direction: xarray.DataArray,
        roughness_length: Optional[xarray.DataArray] = None,
        wind_speed_input_type: TWindInputType = "u10",
    ) -> xarray.DataArray:
        wind = (speed.values, direction.values, wind_speed_input_type)

        if roughness_length is None:
            roughness_length = self.roughness(
                speed, direction, spectrum, wind_speed_input_type=wind_speed_input_type
            )

        wind_input = _bulk_wind_generation(
            spectrum.variance_density.values,
            wind,
            spectrum.depth.values,
            roughness_length.values,
            self._wind_source_term_function,
            self.spectral_grid(spectrum),
            self.parameters,
        )
        return xarray.DataArray(
            data=wind_input,
            dims=spectrum.dims_space_time,
            coords=spectrum.coords_space_time,
        )

    def roughness(
        self,
        speed: xarray.DataArray,
        direction: xarray.DataArray,
        spectrum: FrequencyDirectionSpectrum,
        roughness_length_guess: Optional[xarray.DataArray] = None,
        wind_speed_input_type: TWindInputType = "u10",
    ) -> xarray.DataArray:
        if roughness_length_guess is None:
            roughness_length_guess = xarray.zeros_like(speed) - 1

        wind = (speed.values, direction.values, wind_speed_input_type)

        rougness = _roughness_estimate(
            guess=roughness_length_guess.values,
            variance_density=spectrum.variance_density.values,
            wind=wind,
            depth=spectrum.depth.values,
            wind_source_term_function=self._wind_source_term_function,
            tail_stress_parametrization_function=(
                self._tail_stress_parametrization_function
            ),
            spectral_grid=self.spectral_grid(spectrum),
            parameters=self.parameters,
        )
        return xarray.DataArray(
            data=rougness,
            dims=spectrum.dims_space_time,
            coords=spectrum.coords_space_time,
        )

    def stress(
        self,
        spectrum: FrequencyDirectionSpectrum,
        speed: xarray.DataArray,
        direction: xarray.DataArray,
        roughness_length: Optional[xarray.DataArray] = None,
        wind_speed_input_type: TWindInputType = "u10",
    ) -> xarray.Dataset:
        if roughness_length is None:
            roughness_length = self.roughness(
                speed, direction, spectrum, wind_speed_input_type=wind_speed_input_type
            )

        wind = (speed.values, direction.values, wind_speed_input_type)

        stress = _wave_supported_stress(
            variance_density=spectrum.variance_density.values,
            wind=wind,
            depth=spectrum.depth.values,
            roughness_length=roughness_length.values,
            wind_source_term_function=self._wind_source_term_function,
            tail_stress_parametrization_function=(
                self._tail_stress_parametrization_function
            ),
            spectral_grid=self.spectral_grid(spectrum),
            parameters=self.parameters,
        )

        return xarray.Dataset(
            data_vars={
                "stress": (spectrum.dims_space_time, stress[0]),
                "direction": (spectrum.dims_space_time, stress[1]),
            },
            coords=spectrum.coords_space_time,
        )

    def friction_velocity(
        self,
        spectrum: FrequencyDirectionSpectrum,
        u10: xarray.DataArray,
        direction: xarray.DataArray,
        roughness_length: Optional[xarray.DataArray] = None,
    ) -> xarray.DataArray:
        stress = self.stress(spectrum, u10, direction, roughness_length, "u10")
        return np.sqrt(stress["stress"] / self.parameters["air_density"])

    def drag(
        self,
        spectrum: FrequencyDirectionSpectrum,
        speed: xarray.DataArray,
        direction: xarray.DataArray,
        roughness_length: Optional[xarray.DataArray] = None,
        wind_speed_input_type: TWindInputType = "u10",
    ):
        if wind_speed_input_type == "u10":
            u10 = speed
            u_star = self.friction_velocity(
                spectrum, speed, direction, roughness_length
            )
        else:
            u_star = speed
            roughness = self.roughness(
                speed, direction, spectrum, wind_speed_input_type=wind_speed_input_type
            )
            u10 = (
                u_star * self.parameters["vonkarman_constant"] * np.log(10 / roughness)
            )

        return xarray.DataArray(data=u_star.values**2 / u10.values**2)

    def tail_stress(
        self,
        spectrum: FrequencyDirectionSpectrum,
        speed: xarray.DataArray,
        direction: xarray.DataArray,
        roughness_length: Optional[xarray.DataArray] = None,
        wind_speed_input_type: TWindInputType = "u10",
    ) -> xarray.Dataset:
        if roughness_length is None:
            roughness_length = self.roughness(
                speed, direction, spectrum, wind_speed_input_type=wind_speed_input_type
            )

        wind = (speed.values, direction.values, wind_speed_input_type)
        stress = _tail_supported_stress(
            variance_density=spectrum.variance_density.values,
            wind=wind,
            depth=spectrum.depth.values,
            roughness_length=roughness_length.values,
            tail_stress_parametrization_function=(
                self._tail_stress_parametrization_function
            ),
            spectral_grid=self.spectral_grid(spectrum),
            parameters=self.parameters,
        )

        return xarray.Dataset(
            data_vars={
                "stress": (spectrum.dims_space_time, stress[0]),
                "direction": (spectrum.dims_space_time, stress[1]),
            },
            coords=spectrum.coords_space_time,
        )


# ----------------------------------------------------------------------------------------------------------------------
# Apply to all spatial points
# ----------------------------------------------------------------------------------------------------------------------


@numba.jit(**numba_nocache_parallel)
def _wind_generation(
    variance_density: np.ndarray,
    wind: Tuple[np.ndarray, np.ndarray, TWindInputType],
    depth: np.ndarray,
    roughness_length: np.ndarray,
    wind_source_term_function: Callable,
    spectral_grid: Dict[str, np.ndarray],
    parameters: Mapping,
) -> np.typing.NDArray:
    (
        number_of_points,
        number_of_frequencies,
        number_of_directions,
    ) = variance_density.shape

    generation = np.empty(
        (number_of_points, number_of_frequencies, number_of_directions)
    )
    for point_index in range(number_of_points):
        wind_at_point = (wind[0][point_index], wind[1][point_index], wind[2])
        wind_generation = wind_source_term_function(
            variance_density[point_index, :, :],
            wind_at_point,
            depth[point_index],
            roughness_length[point_index],
            spectral_grid,
            parameters,
        )
        generation[point_index, :, :] = wind_generation
    return generation


@numba.jit(**numba_nocache_parallel)
def _bulk_wind_generation(
    variance_density: np.ndarray,
    wind: Tuple[np.ndarray, np.ndarray, str],
    depth: np.ndarray,
    roughness_length: np.ndarray,
    wind_source_term_function: Callable,
    spectral_grid: Dict[str, np.ndarray],
    parameters: Mapping,
) -> np.typing.NDArray:
    number_of_points = variance_density.shape[0]
    generation = np.empty((number_of_points))

    for point_index in numba.prange(number_of_points):
        wind_at_point = (wind[0][point_index], wind[1][point_index], wind[2])
        wind_generation = wind_source_term_function(
            variance_density=variance_density[point_index, :, :],
            wind=wind_at_point,
            depth=depth[point_index],
            roughness_length=roughness_length[point_index],
            spectral_grid=spectral_grid,
            parameters=parameters,
        )
        generation[point_index] = numba_integrate_spectral_data(
            wind_generation, spectral_grid
        )
    return generation


# ----------------------------------------------------------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------------------------------------------------------


@numba.jit(**numba_default)
def _spectral_grid(
    radian_frequency: np.ndarray,
    radian_direction: np.ndarray,
    frequency_step: np.ndarray,
    direction_step: np.ndarray,
) -> Dict[str, np.ndarray]:
    return {
        "radian_frequency": radian_frequency,
        "radian_direction": radian_direction,
        "frequency_step": frequency_step,
        "direction_step": direction_step,
    }


def _numba_parameters(**kwargs) -> numba.typed.Dict:
    _dict = numba.typed.Dict.empty(
        key_type=numba.types.unicode_type, value_type=numba.types.float64
    )
    for key in kwargs:
        _dict[key] = kwargs[key]

    return _dict


@numba.jit(**numba_default)
def _tail_stress_parametrization_none(
    variance_density: np.ndarray,
    wind: Tuple[np.ndarray, np.ndarray, str],
    depth: np.ndarray,
    roughness_length: np.ndarray,
    wind_source_term_function: Callable,
    spectral_grid: Dict[str, np.ndarray],
    parameters: Mapping,
) -> float:
    return 0.0
