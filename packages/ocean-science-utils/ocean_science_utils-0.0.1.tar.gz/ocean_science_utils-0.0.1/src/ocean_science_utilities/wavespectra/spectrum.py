import numpy as np
import xarray

from typing import (
    Dict,
    Iterator,
    Hashable,
    List,
    Literal,
    Mapping,
    Optional,
    Union,
    TypeVar,
)
from warnings import warn

from ocean_science_utilities.interpolate.dataset import (
    interpolate_dataset_grid,
    interpolate_dataset_along_axis,
)
from ocean_science_utilities.tools.grid import midpoint_rule_step
from ocean_science_utilities.tools.math import wrapped_difference
from ocean_science_utilities.tools.time import to_datetime64
from ocean_science_utilities.wavetheory.lineardispersion import (
    inverse_intrinsic_dispersion_relation,
    intrinsic_group_velocity,
)
from ocean_science_utilities.wavespectra.estimators.estimate import (
    estimate_directional_distribution,
    Estimators,
)
from ocean_science_utilities.wavespectra._tools import (
    numba_fill_zeros_or_nan_in_tail,
    spline_peak_frequency,
    _cdf_interpolate_spline,
)

NAME_F: Literal["frequency"] = "frequency"
NAME_D: Literal["direction"] = "direction"
NAME_T: Literal["time"] = "time"
NAME_E: Literal["variance_density"] = "variance_density"
NAME_a1: Literal["a1"] = "a1"
NAME_b1: Literal["b1"] = "b1"
NAME_a2: Literal["a2"] = "a2"
NAME_b2: Literal["b2"] = "b2"
NAME_LAT: Literal["latitude"] = "latitude"
NAME_LON: Literal["longitude"] = "longitude"
NAME_DEPTH: Literal["depth"] = "depth"
NAMES_2D = (NAME_F, NAME_D, NAME_T, NAME_E, NAME_LAT, NAME_LON, NAME_DEPTH)
NAMES_1D = (
    NAME_F,
    NAME_T,
    NAME_E,
    NAME_LAT,
    NAME_LON,
    NAME_a1,
    NAME_b1,
    NAME_a2,
    NAME_b2,
    NAME_DEPTH,
)
SPECTRAL_VARS = (NAME_E, NAME_a1, NAME_b1, NAME_a2, NAME_b2)
SPECTRAL_MOMENTS = (NAME_a1, NAME_b1, NAME_a2, NAME_b2)
SPECTRAL_DIMS = (NAME_F, NAME_D)
SPACE_TIME_DIMS = (NAME_T, NAME_LON, NAME_LAT)

DatasetWrapperSelf = TypeVar("DatasetWrapperSelf", bound="DatasetWrapper")


class DatasetWrapper:
    """
    A class that wraps a dataset object and passes through some of its primary
    functionality (get/set etc.). Used here mostly to make explicit what parts
    of the Dataset interface we actually expose in frequency objects. Note that
    we do not claim- or try to obtain completeness here. If full capabilities
    of the dataset object are needed we can simple operate directly on the
    dataset object itself.
    """

    def __init__(self: DatasetWrapperSelf, dataset: xarray.Dataset):
        self.dataset = dataset

    def __getitem__(
        self: DatasetWrapperSelf, item: Hashable
    ) -> Union[DatasetWrapperSelf, xarray.DataArray]:
        return self.dataset.__getitem__(item)

    def __setitem__(self: DatasetWrapperSelf, key, value) -> None:
        return self.dataset.__setitem__(key, value)

    def __copy__(self: DatasetWrapperSelf):
        cls = self.__class__
        return cls(self.dataset.copy())

    def __len__(self: DatasetWrapperSelf) -> int:
        return len(self.dataset)

    def copy(self, deep=True):
        if deep:
            return self.__deepcopy__({})
        else:
            return self.__copy__()

    def __deepcopy__(self, memodict):
        cls = self.__class__
        return cls(self.dataset.copy(deep=True))

    def coords(self) -> xarray.core.coordinates.DatasetCoordinates:
        return self.dataset.coords

    def keys(self):
        return self.dataset.keys()

    def __contains__(self, key: object) -> bool:
        return key in self.dataset

    def __iter__(self) -> Iterator[Hashable]:
        return self.dataset.__iter__()

    def sel(self, *args, method="nearest"):
        cls = type(self)
        dataset = xarray.Dataset()
        for var in self.dataset:
            dataset = dataset.assign({var: self.dataset[var].sel(*args, method=method)})
        return cls(dataset=dataset)

    def isel(self, *args, **kwargs):
        cls = type(self)
        dataset = xarray.Dataset()
        for var in self.dataset:
            dataset = dataset.assign({var: self.dataset[var].isel(*args, **kwargs)})
        return cls(dataset=dataset)


WaveSpectrumSelf = TypeVar("WaveSpectrumSelf", bound="WaveSpectrum")


class WaveSpectrum(DatasetWrapper):
    frequency_units = "Hertz"
    angular_units = "Degrees"
    spectral_density_units = "m**2/Hertz"
    angular_convention = (
        "Wave travel direction (going-to), measured anti-clockwise from East"
    )
    bulk_properties = (
        "m0",
        "hm0",
        "tm01",
        "tm02",
        "peak_period",
        "peak_direction",
        "peak_directional_spread",
        "mean_direction",
        "mean_directional_spread",
        "peak_frequency",
        "peak_wavenumber",
        "latitude",
        "longitude",
        "time",
    )

    def __init__(self: WaveSpectrumSelf, dataset: xarray.Dataset):
        super(WaveSpectrum, self).__init__(dataset)

    def __add__(self, other):
        cls = type(self)
        spectrum = cls(self.copy(deep=True).dataset)
        spectrum.dataset[NAME_E] = spectrum.dataset[NAME_E] + other.dataset[NAME_E]
        return spectrum

    def __sub__(self, other):
        cls = type(self)
        spectrum = cls(self.copy(deep=True).dataset)
        spectrum.dataset[NAME_E] = spectrum.dataset[NAME_E] - other.dataset[NAME_E]
        return spectrum

    def __neg__(self):
        """
        Negate self- that is -spectrum
        :return: spectrum with all spectral values taken to have the opposite
            sign.
        """
        cls = type(self)
        spectrum = cls(self.copy(deep=True).dataset)
        spectrum.dataset[NAME_E] = -spectrum.dataset[NAME_E]
        return spectrum

    def __len__(self) -> int:
        return self.number_of_spectra

    def __getitem__(self: WaveSpectrumSelf, item: Hashable) -> WaveSpectrumSelf:
        if isinstance(item, tuple):
            if len(item) < self.ndims:
                raise ValueError(
                    "Indexing requires same number of inputs"
                    f"as dimensions: {self.ndims}"
                )
            space_time_index: Hashable = item[: -len(self.dims_spectral)]
        else:
            if not self.ndims == 1:
                raise ValueError(
                    "Indexing requires same number of inputs"
                    f"as dimensions: {self.ndims}"
                )
            space_time_index = ()

        dataset = xarray.Dataset()
        for var in self.dataset:
            if var in SPECTRAL_VARS:
                dataset = dataset.assign({var: self.dataset[var].__getitem__(item)})
            else:
                if space_time_index:
                    # array
                    dataset = dataset.assign(
                        {var: self.dataset[var].__getitem__(space_time_index)}
                    )
                else:
                    # Scalar
                    dataset = dataset.assign({var: self.dataset[var]})

        for coor in dataset.coords:
            if coor not in dataset.dims:
                dataset = dataset.reset_coords(str(coor))

        cls = type(self)
        return cls(dataset)

    @property
    def ndims(self) -> int:
        return len(self.dims)

    @property
    def frequency_step(self) -> xarray.DataArray:
        prepend = 2 * self.frequency[0] - self.frequency[1]
        append = 2 * self.frequency[-1] - self.frequency[-2]
        diff = np.diff(self.frequency, append=append, prepend=prepend)
        return xarray.DataArray(
            data=(diff[0:-1] * 0.5 + diff[1:] * 0.5),
            dims=NAME_F,
            coords={NAME_F: self.frequency},
        )

    def fillna(self, value=0.0):
        for variable in SPECTRAL_VARS:
            if variable in self.dataset:
                self.dataset[variable] = self.dataset[variable].fillna(value)

    def is_invalid(self) -> xarray.DataArray:
        return self.variance_density.isnull().all(dim=self.dims_spectral)

    def is_valid(self) -> xarray.DataArray:
        return ~self.is_invalid()

    def drop_invalid(self):
        return self._apply_filter(self.is_valid())

    def where(self, condition: xarray.DataArray):
        return self._apply_filter(condition)

    def _apply_filter(self, boolean_mask: xarray.DataArray):
        dataset = xarray.Dataset()
        for var in self.dataset:
            data = self.dataset[var].where(
                boolean_mask.reindex_like(self.dataset[var]), drop=True
            )
            dataset = dataset.assign({var: data})

        cls = type(self)
        return cls(dataset)

    def mean(self, dim, skipna=False):
        """
        Calculate the mean value of the spectrum along the given dimension.
        :param dim: dimension to average over
        :param skipna: whether or not to "skip" nan values; if
            True behaves as np.nanmean
        :return:
        """
        if dim in SPECTRAL_DIMS:
            raise ValueError("Cannot calculate mean over spectral dimensions")

        cls = type(self)
        dataset = xarray.Dataset()
        # Todo: fix averaging over longitude for (prime/anti) meridian issues
        dataset = dataset.assign({dim: self.dataset[dim].mean(dim=dim, skipna=skipna)})
        for x in self.dataset:
            dataset = dataset.assign({x: self.dataset[x].mean(dim=dim, skipna=skipna)})
        return cls(dataset)

    def flatten(self, flattened_coordinate="linear_index"):
        """
        Serialize the non-spectral dimensions creating a single leading dimension
        without a coordinate.
        """

        # Get the current dimensions and shape
        dims = self.dims_space_time
        coords = self.coords_space_time
        shape = self.space_time_shape()
        if len(shape) == 0:
            length = 1
            shape = (1,)
        else:
            length = np.prod(shape)

        # Calculate the flattened shape
        new_shape = (length,)
        new_spectral_shape = (length, *self.spectral_shape())
        new_dims = [flattened_coordinate] + self.dims_spectral

        linear_index = xarray.DataArray(
            data=np.arange(0, length), dims=flattened_coordinate
        )
        indices = np.unravel_index(linear_index.values, shape)

        dataset = {}
        for index, dim in zip(indices, dims):
            dataset[dim] = xarray.DataArray(
                data=coords[dim].values[index], dims=flattened_coordinate
            )

        for name in self.dataset:
            if name in SPECTRAL_VARS:
                x = xarray.DataArray(
                    data=self.dataset[name].values.reshape(new_spectral_shape),
                    dims=new_dims,
                    coords=self.coords_spectral,
                )
            else:
                x = xarray.DataArray(
                    data=self.dataset[name].values.reshape(new_shape),
                    dims=flattened_coordinate,
                )
            dataset[str(name)] = x

        cls = type(self)
        return cls(xarray.Dataset(dataset))

    def sum(self, dim: str, skipna: bool = False):
        """
        Calculate the sum value of the spectrum along the given dimension.
        :param dim: dimension to sum over
        :param skipna: whether or not to "skip" nan values; if True behaves as np.nansum
        :return:
        """

        if dim in SPECTRAL_DIMS:
            raise ValueError("Cannot calculate sum over spectral dimensions")

        cls = type(self)
        dataset = xarray.Dataset()
        # we assign the average coordinate to the dimension we sum over
        dataset = dataset.assign({dim: self.dataset[dim].mean(dim=dim, skipna=skipna)})
        for x in self.dataset:
            dataset = dataset.assign({x: self.dataset[x].sum(dim=dim, skipna=skipna)})
        return cls(dataset)

    def std(self, dim: str, skipna: bool = False):
        """
        Calculate the standard deviation of the spectrum along the given dimension.
        :param dim: dimension to calculate standard deviation over
        :param skipna: whether or not to "skip" nan values; if True behaves as np.nanstd
        :return:
        """
        if dim in SPECTRAL_DIMS:
            raise ValueError(
                "Cannot calculate standard deviation over spectral dimensions"
            )

        cls = type(self)
        dataset = xarray.Dataset()
        # we assign the average coordinate to the dimension we calculate the std over
        dataset = dataset.assign({dim: self.dataset[dim].mean(dim=dim, skipna=skipna)})
        for x in self.dataset:
            dataset = dataset.assign({x: self.dataset[x].std(dim=dim, skipna=skipna)})
        return cls(dataset)

    def shape(self):
        return self.variance_density.shape

    def spectral_shape(self):
        number_of_spectral_dims = len(self.dims_spectral)
        return self.shape()[-number_of_spectral_dims:]

    def space_time_shape(self):
        number_of_spectral_dims = len(self.dims_spectral)
        return self.shape()[:-number_of_spectral_dims]

    def frequency_moment(self, power: int, fmin=0, fmax=np.inf) -> xarray.DataArray:
        """
        Calculate a "frequency moment" over the given range. A frequency moment
        here refers to the integral:

                    Integral-over-frequency-range[ e(f) * f**power ]

        :param power: power of the frequency
        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :return: frequency moment
        """
        _range = self._range(fmin, fmax)

        # Integrate dataset over frequencies. Make sure to fill any NaN entries
        # with 0 before the integration.
        return (
            (self.e.isel({NAME_F: _range}) * self.frequency[_range] ** power)
            .fillna(0)
            .integrate(coord=NAME_F)
        )

    @property
    def number_of_frequencies(self) -> int:
        """
        :return: number of frequencies
        """
        return len(self.frequency)

    @property
    def dims_space_time(self) -> List[str]:
        return [str(x) for x in self.variance_density.dims if x not in (SPECTRAL_DIMS)]

    @property
    def coords_space_time(self) -> Mapping[str, xarray.DataArray]:
        return {dim: self.dataset[dim] for dim in self.dims_space_time}

    @property
    def coords_spectral(self) -> Mapping[str, xarray.DataArray]:
        return {dim: self.dataset[dim] for dim in self.dims_spectral}

    @property
    def dims_spectral(self) -> List[str]:
        return [str(x) for x in self.variance_density.dims if x in (SPECTRAL_DIMS)]

    @property
    def dims(self) -> List[str]:
        return [str(x) for x in self.variance_density.dims]

    @property
    def number_of_spectra(self):
        dims = self.dims_space_time
        if dims:
            shape = 1
            for d in dims:
                shape *= len(self.dataset[d])
            return shape
        else:
            return 1

    @property
    def spectral_values(self) -> xarray.DataArray:
        """
        :return: Spectral levels
        """
        return self.dataset[NAME_E]

    @property
    def radian_frequency(self) -> xarray.DataArray:
        """
        :return: Radian frequency
        """
        data_array = self.dataset[NAME_F] * 2 * np.pi
        data_array.name = "radian_frequency"
        return data_array

    @property
    def latitude(self) -> xarray.DataArray:
        """
        :return: latitudes
        """
        return self.dataset[NAME_LAT]

    @property
    def longitude(self) -> xarray.DataArray:
        """
        :return: longitudes
        """
        return self.dataset[NAME_LON]

    @property
    def time(self) -> xarray.DataArray:
        """
        :return: Time
        """
        return self.dataset[NAME_T]

    @property
    def variance_density(self) -> xarray.DataArray:
        """
        :return: Time
        """
        return self.dataset[NAME_E]

    @property
    def values(self) -> np.ndarray:
        """
        Get the raw np representation of the wave spectrum
        :return: Numpy ndarray of the wave spectrum.
        """
        return self.dataset[NAME_E].values

    @property
    def e(self) -> xarray.DataArray:
        """
        :return: 1D spectral values (directionally integrated spectrum).
            Equivalent to self.spectral_values if this is a 1D spectrum.
        """
        return self.dataset[NAME_E]

    @property
    def a1(self) -> xarray.DataArray:
        """
        :return: normalized Fourier moment cos(theta)
        """
        return self.dataset[NAME_a1]

    @property
    def b1(self) -> xarray.DataArray:
        """
        :return: normalized Fourier moment sin(theta)
        """
        return self.dataset[NAME_b1]

    @property
    def a2(self) -> xarray.DataArray:
        """
        :return: normalized Fourier moment cos(2*theta)
        """
        return self.dataset[NAME_a2]

    @property
    def b2(self) -> xarray.DataArray:
        """
        :return: normalized Fourier moment sin(2*theta)
        """
        return self.dataset[NAME_b2]

    @property
    def A1(self) -> xarray.DataArray:
        """
        :return: Fourier moment cos(theta)
        """
        return self.a1 * self.e

    @property
    def B1(self) -> xarray.DataArray:
        """
        :return: Fourier moment sin(theta)
        """
        return self.b1 * self.e

    @property
    def A2(self) -> xarray.DataArray:
        """
        :return: Fourier moment cos(2*theta)
        """
        return self.a2 * self.e

    @property
    def B2(self) -> xarray.DataArray:
        """
        :return: Fourier moment sin(2*theta)
        """
        return self.b2 * self.e

    @property
    def frequency(self) -> xarray.DataArray:
        """
        :return: Frequencies (Hz)
        """
        return self.dataset[NAME_F]

    def m0(self, fmin=0, fmax=np.inf) -> xarray.DataArray:
        """
        Zero order frequency moment. Also referred to as variance or energy.

        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :return: variance/energy
        """
        return self.frequency_moment(0, fmin, fmax)

    def m1(self, fmin=0, fmax=np.inf) -> xarray.DataArray:
        """
        First order frequency moment. Primarily used in calculating a mean
        period measure (Tm01)

        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :return: first order frequency moment.
        """
        return self.frequency_moment(1, fmin, fmax)

    def wave_speed(self) -> xarray.DataArray:
        """
        :return:
        """
        # Note we multiply inverse wavenumber with frequency to force xarray to return
        # a number_of_points by by number of frequencies data structure.
        return (1 / self.wavenumber) * self.radian_frequency

    def wave_age(self, windspeed):
        return self.peak_wave_speed() / windspeed

    def peak_wave_speed(self) -> xarray.DataArray:
        return 2 * np.pi * self.peak_frequency() / self.peak_wavenumber

    @property
    def wavenumber_density(self) -> xarray.DataArray:
        return self.variance_density * self.group_velocity / (np.pi * 2)

    @property
    def saturation_spectrum(self) -> xarray.DataArray:
        return self.wavenumber_density * self.wavenumber**3

    @property
    def slope_spectrum(self) -> xarray.DataArray:
        return self.variance_density * self.wavenumber**2

    def mean_squared_slope(self, fmin=0, fmax=np.inf) -> xarray.DataArray:
        _range = self._range(fmin, fmax)

        # Integrate dataset over frequencies. Make sure to fill any NaN entries with
        # 0 before the integration.
        return (
            self.slope_spectrum.fillna(0).isel({NAME_F: _range}).integrate(coord=NAME_F)
        )

    def m2(self, fmin=0, fmax=np.inf) -> xarray.DataArray:
        """
        Second order frequency moment. Primarily used in calculating the zero
        crossing period (Tm02)

        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :return: Second order frequency moment.
        """
        return self.frequency_moment(2, fmin, fmax)

    def hm0(self, fmin=0, fmax=np.inf) -> xarray.DataArray:
        """
        Significant wave height estimated from the spectrum, i.e. waveheight
        h estimated from variance m0. Common notation in literature.

        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :return: Significant wave height
        """
        return xarray.DataArray(4 * np.sqrt(self.m0(fmin, fmax)))

    def tm01(self, fmin=0, fmax=np.inf) -> xarray.DataArray:
        """
        Mean period, estimated as the inverse of the center of mass of the
        spectral curve under the 1d spectrum.

        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :return: Mean period
        """
        return self.m0(fmin, fmax) / self.m1(fmin, fmax)

    def tm02(self, fmin=0, fmax=np.inf) -> xarray.DataArray:
        """
        Zero crossing period based on Rice's spectral estimate.

        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :return: Zero crossing period
        """
        return xarray.DataArray(np.sqrt(self.m0(fmin, fmax) / self.m2(fmin, fmax)))

    def peak_index(self, fmin: float = 0, fmax: float = np.inf) -> xarray.DataArray:
        """
        Index of the peak frequency of the 1d spectrum within the given range
        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :return: peak indices
        """
        return xarray.DataArray(
            self.e.where(self._range(fmin, fmax), 0).argmax(dim=NAME_F)
        )

    def peak_frequency(
        self, fmin=0.0, fmax=np.inf, use_spline=False, **kwargs
    ) -> xarray.DataArray:
        """
        Peak frequency of the spectrum, i.e. frequency at which the spectrum
        obtains its maximum.

        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :param use_spline: Use a spline based interpolation and determine peak
            frequency from the spline. This
        allows for a continuous estimate of the peak frequency. WARNING: if True the
        fmin and fmax paramteres are IGNORED
        :return: peak frequency
        """
        if use_spline:
            if not fmin == 0.0 or np.isfinite(fmax):
                warn(
                    "The fmin and fmax parameters are ignored"
                    "if use_spline is set to True"
                )

            data = spline_peak_frequency(self.frequency.values, self.e.values, **kwargs)
            if len(self.dims_space_time) == 0:
                data = data[0]

            return xarray.DataArray(
                data=data,
                coords=self.coords_space_time,
                dims=self.dims_space_time,
            )
        else:
            return self.dataset[NAME_F][self.peak_index(fmin, fmax)]

    def peak_angular_frequency(self, fmin=0, fmax=np.inf) -> xarray.DataArray:
        """
        Peak frequency of the spectrum, i.e. frequency at which the spectrum
        obtains its maximum.

        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :return: peak frequency
        """
        return self.peak_frequency(fmin, fmax) * np.pi * 2

    def peak_period(
        self, fmin=0, fmax=np.inf, use_spline=False, **kwargs
    ) -> xarray.DataArray:
        """
        Peak period of the spectrum, i.e. period at which the spectrum
        obtains its maximum.

        :param fmin: minimum frequency
        :param fmax: maximum frequency
        :return: peak period
        """
        peak_period = 1 / self.peak_frequency(
            fmin, fmax, use_spline=use_spline, **kwargs
        )
        peak_period.name = "peak period"
        try:
            peak_period = peak_period.drop("frequency")  # type: ignore
        except Exception:
            pass
        return peak_period

    def peak_direction(self, fmin=0, fmax=np.inf) -> xarray.DataArray:
        index = self.peak_index(fmin, fmax)
        return self._mean_direction(
            self.a1.isel(**{NAME_F: index}),  # type: ignore
            self.b1.isel(**{NAME_F: index}),  # type: ignore
        )

    def peak_directional_spread(self, fmin=0, fmax=np.inf) -> xarray.DataArray:
        index = self.peak_index(fmin, fmax)
        a1 = self.a1.isel(**{NAME_F: index})  # type: ignore
        b1 = self.b1.isel(**{NAME_F: index})  # type: ignore
        return self._spread(a1, b1)

    @staticmethod
    def _mean_direction(a1: xarray.DataArray, b1: xarray.DataArray) -> xarray.DataArray:
        return xarray.DataArray(np.arctan2(b1, a1) * 180 / np.pi)

    @staticmethod
    def _spread(a1: xarray.DataArray, b1: xarray.DataArray) -> xarray.DataArray:
        return xarray.DataArray(
            np.sqrt(2 - 2 * np.sqrt(a1**2 + b1**2)) * 180 / np.pi
        )

    @property
    def mean_direction_per_frequency(self) -> xarray.DataArray:
        return self._mean_direction(self.a1, self.b1)

    @property
    def mean_spread_per_frequency(self) -> xarray.DataArray:
        return self._spread(self.a1, self.b1)

    def _spectral_weighted(self, property: xarray.DataArray, fmin=0, fmax=np.inf):
        range = {NAME_F: self._range(fmin, fmax)}

        property = property.fillna(0)
        return np.trapz(
            property.isel(**range) * self.e.isel(**range),  # type: ignore
            self.frequency[range],
        ) / self.m0(fmin, fmax)

    def mean_direction(self, fmin=0, fmax=np.inf):
        return self._mean_direction(self.mean_a1(fmin, fmax), self.mean_b1(fmin, fmax))

    def mean_directional_spread(self, fmin=0, fmax=np.inf):
        return self._spread(self.mean_a1(fmin, fmax), self.mean_b1(fmin, fmax))

    def mean_a1(self, fmin=0, fmax=np.inf):
        return self._spectral_weighted(self.a1, fmin, fmax)

    def mean_b1(self, fmin=0, fmax=np.inf):
        return self._spectral_weighted(self.b1, fmin, fmax)

    def mean_a2(self, fmin=0, fmax=np.inf):
        return self._spectral_weighted(self.a2, fmin, fmax)

    def mean_b2(self, fmin=0, fmax=np.inf):
        return self._spectral_weighted(self.b2, fmin, fmax)

    @property
    def depth(self) -> xarray.DataArray:
        depth = self.dataset[NAME_DEPTH]
        return xarray.where(depth.isnull(), np.inf, depth)

    @property
    def group_velocity(self) -> xarray.DataArray:
        depth = self.depth.expand_dims(dim=NAME_F, axis=-1).values
        k = self.wavenumber.values
        depth = depth * np.ones(k.shape)

        # Construct the output coordinates and dimension of the data array
        return_dimensions = (*self.dims_space_time, NAME_F)
        coords = {}
        for dim in return_dimensions:
            coords[dim] = self.dataset[dim].values

        return xarray.DataArray(
            data=intrinsic_group_velocity(k, depth),
            dims=return_dimensions,
            coords=coords,
        )

    @property
    def wavenumber(self) -> xarray.DataArray:
        """
        Determine the wavenumbers for the frequencies in the spectrum. Note that since
        the dispersion relation depends on depth the returned wavenumber array has the
        dimensions associated with the depth array by the frequency dimension.

        :return: wavenumbers
        """

        # For numba (used in the dispersion relation) we need raw np arrays of
        # the correct dimension
        depth = self.depth.expand_dims(dim=NAME_F, axis=-1).values
        radian_frequency = self.radian_frequency.expand_dims(dim=self.depth.dims).values

        # Broadcasting does not work inside the numba implementaiton, we explicitly
        # need to construct arrays of the correct input dimension.
        depth_shape = depth.shape
        radian_frequency_shape = radian_frequency.shape

        depth = depth * np.ones(radian_frequency_shape)
        radian_frequency = np.ones(depth_shape) * radian_frequency

        # Construct the output coordinates and dimension of the data array
        return_dimensions = (*self.dims_space_time, NAME_F)
        coords = {}
        for dim in return_dimensions:
            coords[dim] = self.dataset[dim].values

        return xarray.DataArray(
            data=inverse_intrinsic_dispersion_relation(radian_frequency, depth),
            dims=return_dimensions,
            coords=coords,
        )

    @property
    def wavelength(self) -> xarray.DataArray:
        return 2 * np.pi / self.wavenumber

    @property
    def peak_wavenumber(self) -> xarray.DataArray:
        index = self.peak_index()
        # Construct the output coordinates and dimension of the data array
        coords = {}
        for dim in self.dims_space_time:
            coords[dim] = self.dataset[dim].values

        return xarray.DataArray(
            data=inverse_intrinsic_dispersion_relation(
                self.radian_frequency[index].values, self.depth.values
            ),
            dims=self.dims_space_time,
            coords=coords,
        )

    def bulk_variables(self) -> xarray.Dataset:
        dataset = xarray.Dataset()
        dataset["significant_waveheight"] = self.significant_waveheight
        dataset["mean_period"] = self.mean_period
        dataset["peak_period"] = self.peak_period()
        dataset["peak_direction"] = self.peak_direction()
        dataset["peak_directional_spread"] = self.peak_directional_spread()
        dataset["mean_direction"] = self.mean_direction()
        dataset["mean_directional_spread"] = self.mean_directional_spread()
        dataset["peak_frequency"] = self.peak_frequency()
        dataset["latitude"] = self.latitude
        dataset["longitude"] = self.longitude
        dataset["timestamp"] = self.time
        return dataset

    @property
    def significant_waveheight(self) -> xarray.DataArray:
        return self.hm0()

    @property
    def mean_period(self) -> xarray.DataArray:
        return self.tm01()

    @property
    def zero_crossing_period(self) -> xarray.DataArray:
        return self.tm02()

    def cdf(self) -> xarray.DataArray:
        """

        :return:
        """
        frequency_step = self.frequency_step
        integration_frequencies = np.concatenate(
            ([0], np.cumsum(frequency_step.values))
        )
        integration_frequencies = (
            integration_frequencies
            - frequency_step.values[0] / 2
            + self.frequency.values[0]
        )
        values = (self.variance_density * frequency_step).values

        frequency_axis = self.dims.index(NAME_F)

        cumsum = np.cumsum(values, axis=frequency_axis)
        # cumsum =  self.variance_density.cumulative_integrate(coord=NAME_F)
        # return cumsum
        shape = list(cumsum.shape)
        shape[frequency_axis] = 1

        cumsum = np.concatenate((np.zeros(shape), cumsum), axis=frequency_axis)

        coords = {str(coor): self.coords()[coor].values for coor in self.coords()}
        coords[NAME_F] = integration_frequencies
        return xarray.DataArray(data=cumsum, dims=self.dims, coords=coords)

    def interpolate(
        self,
        coordinates: Dict[str, Union[xarray.DataArray, np.ndarray]],
        extrapolation_value: float = 0.0,
    ):
        dataset = self.__class__(
            xarray.Dataset(interpolate_dataset_grid(coordinates, self.dataset))
        )
        dataset.fillna(extrapolation_value)
        return dataset

    def extrapolate_tail(
        self,
        end_frequency,
        power=None,
        tail_energy=None,
        tail_bounds=None,
        tail_moments=None,
        tail_frequency=None,
    ) -> "FrequencySpectrum":
        """
        Extrapolate the tail using the given power
        :param end_frequency: frequency to extrapolate to
        :param power: power to use. If None, a best fit -4 or -5 tail is used.
        :return:
        """
        e = self.e
        a1 = self.a1
        b1 = self.b1
        a2 = self.a2
        b2 = self.b2

        frequency = self.frequency.values
        frequency_delta = frequency[-1] - frequency[-2]
        n = int((end_frequency - frequency[-1]) / frequency_delta) + 1

        fstart = frequency[-1] + frequency_delta
        fend = frequency[-1] + n * frequency_delta

        if tail_frequency is None:
            tail_frequency = np.linspace(fstart, fend, n, endpoint=True)

        tail_frequency = xarray.DataArray(
            data=tail_frequency, coords={"frequency": tail_frequency}, dims="frequency"
        )
        variance_density = xarray.concat(
            (e, e.isel(frequency=-1) * xarray.zeros_like(tail_frequency)),
            dim="frequency",
        )

        tail_a1 = a1.isel(frequency=-1) if tail_moments is None else tail_moments["a1"]
        tail_b1 = b1.isel(frequency=-1) if tail_moments is None else tail_moments["b1"]
        tail_a2 = a2.isel(frequency=-1) if tail_moments is None else tail_moments["a2"]
        tail_b2 = b2.isel(frequency=-1) if tail_moments is None else tail_moments["b2"]

        a1 = xarray.concat(
            (a1, tail_a1 * xarray.ones_like(tail_frequency)), dim="frequency"
        )
        b1 = xarray.concat(
            (b1, tail_b1 * xarray.ones_like(tail_frequency)), dim="frequency"
        )
        a2 = xarray.concat(
            (a2, tail_a2 * xarray.ones_like(tail_frequency)), dim="frequency"
        )
        b2 = xarray.concat(
            (b2, tail_b2 * xarray.ones_like(tail_frequency)), dim="frequency"
        )

        if tail_energy is not None:
            if isinstance(tail_energy, xarray.DataArray):
                tail_energy = tail_energy.values

            tail_information = (tail_bounds, tail_energy)
        else:
            tail_information = None

        variance_density = xarray.DataArray(
            data=numba_fill_zeros_or_nan_in_tail(
                variance_density.values,
                variance_density.frequency.values,
                power,
                tail_information=tail_information,
            ),
            dims=a1.dims,
            coords=a1.coords,
        )

        dataset = xarray.Dataset(
            {
                "variance_density": variance_density,
                "a1": a1,
                "b1": b1,
                "a2": a2,
                "b2": b2,
            }
        )

        for name in self.dataset:
            if name in SPECTRAL_VARS:
                continue
            else:
                dataset = dataset.assign({name: self.dataset[name]})

        return FrequencySpectrum(dataset)

    def bandpass(self, fmin: float = 0, fmax: float = np.inf):
        dataset = xarray.Dataset()

        for name in self.dataset:
            if name in SPECTRAL_VARS:
                data = self.dataset[name].where(
                    (self.frequency >= fmin) & (self.frequency < fmax), drop=True
                )
                dataset = dataset.assign({name: data})
            else:
                dataset = dataset.assign({name: self.dataset[name]})
        cls = type(self)
        return cls(dataset)

    def interpolate_frequency(
        self,
        new_frequencies: Union[xarray.DataArray, np.ndarray],
        extrapolation_value: float = 0.0,
    ):
        obj = self.__class__(
            interpolate_dataset_along_axis(
                new_frequencies, self.dataset, coordinate_name="frequency"
            )
        )
        obj.fillna(extrapolation_value)
        return obj

    def _range(self, fmin=0.0, fmax=np.inf) -> np.ndarray:
        return (self.dataset[NAME_F].values >= fmin) & (
            self.dataset[NAME_F].values < fmax
        )

    def save_as_netcdf(self, path):
        self.dataset.to_netcdf(path)

    def multiply(
        self,
        array: np.ndarray,
        dimensions: Optional[List[str]] = None,
        inplace: bool = False,
    ):
        """
        Multiply the variance density with the given np array. Broadcasting is
        performed automatically if dimensions are provided. If no dimensions are
        provided the array needs to have the exact same shape as the variance
        density array.

        :param array: Array to multiply with variance density
        :param dimension: Dimensions of the array
        :return: self
        """
        if inplace:
            output = self
        else:
            output = self.copy()

        coords = {}
        shape = array.shape
        if dimensions is None:
            if shape != self.shape():
                raise ValueError(
                    "If no dimensions are provided the array must have the exact same"
                    "shape as the variance density array."
                )

            output.dataset[NAME_E] = self.dataset[NAME_E] * array
            return output

        if len(shape) != len(dimensions):
            raise ValueError(
                "The dimensions of the input array must match the number of"
                "dimension labels"
            )

        for length, dimension in zip(shape, dimensions):
            if dimension not in self.dims:
                raise ValueError(
                    f"Dimension {dimension} not a valid dimension of the"
                    "spectral object."
                )
            coords[dimension] = self.dataset[dimension].values

            if len(self.dataset[dimension].values) != length:
                raise ValueError(
                    f"Array length along the dimension {dimension} does not match the"
                    " length of the coordinate of the same name in the spctral object."
                )

        data = xarray.DataArray(data=array, coords=coords, dims=dimensions)
        output.dataset[NAME_E] = self.dataset[NAME_E] * data
        return output


class FrequencyDirectionSpectrum(WaveSpectrum):
    def __init__(self, dataset: xarray.Dataset):
        super(FrequencyDirectionSpectrum, self).__init__(dataset)
        for name in NAMES_2D:
            if name not in dataset and name not in dataset.coords:
                raise ValueError(
                    f"Required variable/coordinate {name} is"
                    f" not specified in the dataset"
                )

    def __len__(self):
        return int(np.prod(self.spectral_values.shape[:-2]))

    @property
    def direction_step(self) -> xarray.DataArray:
        difference = wrapped_difference(
            np.diff(self.direction.values, append=self.direction[0]), period=360
        )
        return xarray.DataArray(
            data=difference, coords={NAME_D: self.direction.values}, dims=[NAME_D]
        )

    @property
    def radian_direction(self) -> xarray.DataArray:
        data_array = self.dataset[NAME_D] * np.pi / 180
        data_array.name = "radian_direction"
        return data_array

    def _directionally_integrate(
        self, data_array: xarray.DataArray
    ) -> xarray.DataArray:
        return (data_array * self.direction_step).sum(NAME_D, skipna=True)

    @property
    def e(self) -> xarray.DataArray:
        return self._directionally_integrate(self.dataset[NAME_E])

    @property
    def a1(self) -> xarray.DataArray:
        return (
            self._directionally_integrate(
                self.dataset[NAME_E] * np.cos(self.radian_direction)
            )
            / self.e
        )

    @property
    def b1(self) -> xarray.DataArray:
        return (
            self._directionally_integrate(
                self.dataset[NAME_E] * np.sin(self.radian_direction)
            )
            / self.e
        )

    @property
    def a2(self) -> xarray.DataArray:
        return (
            self._directionally_integrate(
                self.dataset[NAME_E] * np.cos(2 * self.radian_direction)
            )
            / self.e
        )

    @property
    def b2(self) -> xarray.DataArray:
        return (
            self._directionally_integrate(
                self.dataset[NAME_E] * np.sin(2 * self.radian_direction)
            )
            / self.e
        )

    @property
    def direction(self) -> xarray.DataArray:
        return self.dataset[NAME_D]

    def as_frequency_spectrum(self):
        dataset = {
            "a1": self.a1,
            "b1": self.b1,
            "a2": self.a2,
            "b2": self.b2,
            "variance_density": self.e,
        }
        for name in self.dataset:
            if name not in SPECTRAL_VARS:
                dataset[str(name)] = self.dataset[name]

        return FrequencySpectrum(xarray.Dataset(dataset))

    def spectrum_1d(self):
        """
        Will be depricated
        :return:
        """
        warn(
            'spectrum_1d method will be removed, use "as_frequency_spectrum" instead',
            DeprecationWarning,
            stacklevel=2,
        )
        return self.as_frequency_spectrum()

    def differentiate(self, coordinate=None, **kwargs) -> "FrequencyDirectionSpectrum":
        if coordinate is None:
            coordinate = "time"

        if coordinate not in self.dataset:
            raise ValueError(f"Coordinate {coordinate} does not exist in the dataset")

        data = {
            NAME_E: (
                self.dims,
                self.variance_density.differentiate(
                    coordinate, datetime_unit="s", **kwargs
                ).values,
            )
        }
        for x in self.dataset:
            if x in SPECTRAL_VARS:
                continue
            data[x] = (self.dims_space_time, self.dataset[x].values)  # type: ignore

        return FrequencyDirectionSpectrum(
            xarray.Dataset(data_vars=data, coords=self.coords())
        )

    @property
    def number_of_directions(self) -> int:
        return len(self.direction)


class FrequencySpectrum(WaveSpectrum):
    def __init__(self, dataset: xarray.Dataset):
        super(FrequencySpectrum, self).__init__(dataset)
        for name in NAMES_1D:
            if name not in dataset and name not in dataset.coords:
                raise ValueError(
                    f"Required variable/coordinate {name} is"
                    f" not specified in the dataset"
                )

    def __len__(self):
        return int(np.prod(self.spectral_values.shape[:-1]))

    def interpolate_frequency(
        self: "FrequencySpectrum",
        new_frequencies: Union[xarray.DataArray, np.ndarray],
        extrapolation_value=0.0,
        method: Literal["nearest", "linear", "spline"] = "linear",
        **kwargs,
    ) -> "FrequencySpectrum":
        if isinstance(new_frequencies, xarray.DataArray):
            new_frequencies = new_frequencies.values

        if method == "spline":
            self.fillna(0.0)
            frequency_axis = self.dims.index(NAME_F)
            interpolated_data = cumulative_frequency_interpolation_1d_variable(
                new_frequencies, self.dataset, frequency_axis=frequency_axis, **kwargs
            )
            object = FrequencySpectrum(interpolated_data)
            object.fillna(extrapolation_value)
            return object
        elif method == "linear":
            return self.interpolate(
                {NAME_F: new_frequencies},
                extrapolation_value=extrapolation_value,
                nearest_neighbour=False,
            )
        elif method == "nearest":
            return self.interpolate(
                {NAME_F: new_frequencies},
                extrapolation_value=extrapolation_value,
                nearest_neighbour=True,
            )
        else:
            raise ValueError(f"Unknown interpolation method: {method}")

    def interpolate(
        self: "FrequencySpectrum",
        coordinates,
        extrapolation_value=0.0,
        nearest_neighbour=False,
    ) -> "FrequencySpectrum":
        """

        :param coordinates:
        :return:
        """
        _dataset = xarray.Dataset()
        _moments = [NAME_a1, NAME_b1, NAME_a2, NAME_b2]

        # For physical reasons it is better to interpolate the scaled moments -
        # as opposed to the normalized moments. For the dataset we interpolate
        # we set a1: to A1 etc. Afterwards we scale the output back to the normalized
        # state.
        for name in self.dataset:
            _name = str(name)
            if _name in _moments:
                _dataset = _dataset.assign({_name: getattr(self, _name) * self.e})
            else:
                _dataset = _dataset.assign({_name: self.dataset[_name]})

        interpolated_data = xarray.Dataset(interpolate_dataset_grid(
            coordinates, _dataset, nearest_neighbour
        ))
        for name in _moments:
            interpolated_data[name] = (
                interpolated_data[name] / interpolated_data[NAME_E]
            )

        object = FrequencySpectrum(interpolated_data)
        object.fillna(extrapolation_value)
        return object

    def down_sample(self, frequencies):
        cdf = self.cdf()

        frequency_step = midpoint_rule_step(frequencies)
        sampling_frequencies = np.concatenate(([0], np.cumsum(frequency_step)))
        sampling_frequencies = (
            sampling_frequencies - frequency_step[0] / 2 + frequencies[0]
        )

        dims = self.dims
        sampled_cdf = cdf.sel({"frequency": sampling_frequencies}, method="nearest")
        data = {
            NAME_E: (dims, sampled_cdf.diff(dim="frequency").values / frequency_step),
            NAME_a1: (
                dims,
                self.a1.sel({"frequency": frequencies}, method="nearest").values,
            ),
            NAME_b1: (
                dims,
                self.b1.sel({"frequency": frequencies}, method="nearest").values,
            ),
            NAME_a2: (
                dims,
                self.a2.sel({"frequency": frequencies}, method="nearest").values,
            ),
            NAME_b2: (
                dims,
                self.b2.sel({"frequency": frequencies}, method="nearest").values,
            ),
        }

        coords = {x: self.dataset[x].values for x in self.dims}
        coords[NAME_F] = frequencies

        for x in self.dataset:
            if x in SPECTRAL_VARS:
                continue
            data[x] = (self.dims_space_time, self.dataset[x].values)

        return FrequencySpectrum(xarray.Dataset(data_vars=data, coords=coords))

    def as_frequency_direction_spectrum(
        self,
        number_of_directions,
        method: Estimators = "mem2",
        solution_method="scipy",
    ) -> "FrequencyDirectionSpectrum":
        direction = np.linspace(0, 360, number_of_directions, endpoint=False)

        output_array = (
            estimate_directional_distribution(
                self.a1.values,
                self.b1.values,
                self.a2.values,
                self.b2.values,
                direction,
                method=method,
                solution_method=solution_method,
            )
            * self.e.values[..., None]
        )

        dims = self.dims_space_time + [NAME_F, NAME_D]
        coords = {x: self.dataset[x].values for x in self.dims}
        coords[NAME_D] = direction

        data = {NAME_E: (dims, output_array)}
        for x in self.dataset:
            if x in SPECTRAL_VARS:
                continue
            data[x] = (self.dims_space_time, self.dataset[x].values)  # type: ignore

        return FrequencyDirectionSpectrum(xarray.Dataset(data_vars=data, coords=coords))


def create_1d_spectrum(
    frequency: np.ndarray,
    variance_density: np.ndarray,
    time: Union[np.ndarray, float],
    latitude: Union[np.ndarray, float],
    longitude: Union[np.ndarray, float],
    a1: Optional[np.ndarray] = None,
    b1: Optional[np.ndarray] = None,
    a2: Optional[np.ndarray] = None,
    b2: Optional[np.ndarray] = None,
    depth: Union[np.ndarray, float] = np.inf,
    dims=(NAME_T, NAME_F),
) -> FrequencySpectrum:
    if a1 is None:
        a1 = np.nan + np.ones_like(variance_density)
    if b1 is None:
        b1 = np.nan + np.ones_like(variance_density)
    if a2 is None:
        a2 = np.nan + np.ones_like(variance_density)
    if b2 is None:
        b2 = np.nan + np.ones_like(variance_density)

    variables = {
        NAME_T: np.atleast_1d(to_datetime64(time)),  # type: ignore
        NAME_LAT: np.atleast_1d(latitude),
        NAME_LON: np.atleast_1d(longitude),
        NAME_DEPTH: np.atleast_1d(depth),
        NAME_F: frequency,
        NAME_E: variance_density,
        NAME_a1: a1,
        NAME_b1: b1,
        NAME_a2: a2,
        NAME_b2: b2,
    }

    return FrequencySpectrum(create_spectrum_dataset(dims, variables))


def create_2d_spectrum(
    frequency: np.ndarray,
    direction: np.ndarray,
    variance_density: np.ndarray,
    time,
    latitude: Union[np.ndarray, float, None],
    longitude: Union[np.ndarray, float, None],
    dims=(NAME_T, NAME_F, NAME_D),
    depth: Union[np.ndarray, float] = np.inf,
) -> FrequencyDirectionSpectrum:
    """
    :param frequency:
    :param direction:
    :param variance_density:
    :param time:
    :param latitude:
    :param longitude:
    :param dims:
    :param depth:
    :return:
    """

    variables = {
        NAME_T: np.atleast_1d(to_datetime64(time)),  # type: ignore
        NAME_LAT: np.atleast_1d(latitude),  # type: ignore
        NAME_LON: np.atleast_1d(longitude),  # type: ignore
        NAME_DEPTH: np.atleast_1d(depth),
        NAME_F: frequency,
        NAME_D: direction,
        NAME_E: variance_density,
    }
    return FrequencyDirectionSpectrum(create_spectrum_dataset(dims, variables))


def create_spectrum_dataset(dims, variables) -> xarray.Dataset:
    independent_variables = []
    for dim in dims:
        if dim in variables:
            independent_variables.append(dim)

    dependent_variables = [x for x in variables if x not in independent_variables]

    spectral_coords = {k: variables[k] for k in independent_variables}
    spatial_coords = {
        k: variables[k] for k in independent_variables if k not in SPECTRAL_DIMS
    }

    dataset = xarray.Dataset()
    for variable in dependent_variables:
        if variable in SPECTRAL_VARS:
            coords = spectral_coords
        else:
            coords = spatial_coords
        dims = [k for k in coords]

        if dims:
            dataset = dataset.assign(
                {
                    variable: xarray.DataArray(
                        data=variables[variable], dims=dims, coords=coords
                    )
                }
            )

        else:
            if len(variables[variable]) == 1:
                # If no coordinate is known, and the variable has length 1, we add it
                # as a scalar.
                data = variables[variable][0]
            else:
                # otherwise we add without coordinate/dimension.
                data = xarray.DataArray(data=variables[variable])

            dataset = dataset.assign({variable: data})
    return dataset


def load_spectrum_from_netcdf(
    filename_or_obj,
) -> Union[FrequencySpectrum, FrequencyDirectionSpectrum]:
    """
    Load a spectrum from netcdf file
    :param filename_or_obj:
    :return:
    """
    dataset = xarray.open_dataset(filename_or_obj=filename_or_obj)
    if NAME_D in dataset.coords:
        return FrequencyDirectionSpectrum(dataset=dataset)
    else:
        return FrequencySpectrum(dataset=dataset)


def fill_zeros_or_nan_in_tail(
    spectrum: WaveSpectrum,
    power=None,
    tail_energy=None,
    tail_bounds=None,
) -> FrequencySpectrum:
    variance_density = spectrum.e
    a1 = spectrum.a1
    b1 = spectrum.b1
    a2 = spectrum.a2
    b2 = spectrum.b2

    if tail_energy is not None:
        if isinstance(tail_energy, xarray.DataArray):
            tail_energy = tail_energy.values

        tail_information = (tail_bounds, tail_energy)
    else:
        tail_information = None

    variance_density = xarray.DataArray(
        data=numba_fill_zeros_or_nan_in_tail(
            variance_density.values,
            variance_density.frequency.values,
            power,
            tail_information=tail_information,
        ),
        dims=a1.dims,
        coords=a1.coords,
    )

    dataset = xarray.Dataset(
        {
            "variance_density": variance_density,
            "a1": a1,
            "b1": b1,
            "a2": a2,
            "b2": b2,
        }
    )

    for name in spectrum.dataset:
        if name in SPECTRAL_VARS:
            continue
        else:
            dataset = dataset.assign({name: spectrum.dataset[name]})

    return FrequencySpectrum(dataset)


def cumulative_frequency_interpolation_1d_variable(
    interpolation_frequency, dataset: xarray.Dataset, **kwargs
):
    """
    To interpolate the spectrum we first calculate a cumulative density function from
    the spectrum (which is essentialya pdf). We then interpolate the CDF function with
    a spline and differentiate the result.

    :param interpolation_frequency:
    :param dataset:
    :return:
    """

    _dataset = xarray.Dataset()

    # Copy over all non spectral vars
    for name in dataset:
        _name = str(name)
        if _name not in SPECTRAL_VARS:
            _dataset = _dataset.assign({_name: dataset[_name]})

    coords = {
        str(_coor_name): dataset[str(_coor_name)]
        for _coor_name in dataset[NAME_E].coords
    }
    coords[NAME_F] = interpolation_frequency
    dims = dataset[NAME_E].dims

    # Interpolate energy
    interpolated_cdf_spline = _cdf_interpolate_spline(
        dataset[NAME_F].values,
        dataset[NAME_E].values,
        monotone_interpolation=kwargs.get("monotone_interpolation", True),
        frequency_axis=kwargs.get("frequency_axis", -1),
    )
    interpolated_energy = interpolated_cdf_spline.derivative()(interpolation_frequency)

    _dataset = _dataset.assign(
        {
            NAME_E: xarray.DataArray(
                data=interpolated_energy,
                coords=coords,
                dims=dims,
            )
        }
    )

    msk = interpolated_energy > 0

    for _name in SPECTRAL_MOMENTS:
        interpolated_densities_spline = _cdf_interpolate_spline(
            dataset[NAME_F].values,
            dataset[_name].values * dataset[NAME_E].values,
            monotone_interpolation=kwargs.get("monotone_interpolation_moments", False),
        )
        interpolated_densities = interpolated_densities_spline.derivative()(
            interpolation_frequency
        )
        # Avoid division by zero
        interpolated_densities[msk] = (
            interpolated_densities[msk] / interpolated_energy[msk]
        )

        _dataset = _dataset.assign(
            {
                _name: xarray.DataArray(
                    data=interpolated_densities,
                    coords=coords,
                    dims=dims,
                )
            }
        )

    return _dataset
