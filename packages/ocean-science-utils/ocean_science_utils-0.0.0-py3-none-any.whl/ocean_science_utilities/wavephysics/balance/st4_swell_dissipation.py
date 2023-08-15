import numpy as np
import xarray

from scipy.special import kelvin  # type: ignore
from typing import Any, Dict, Optional

from ocean_science_utilities.wavephysics.fluidproperties import (
    AIR,
    WATER,
    FluidProperties,
    GRAVITATIONAL_ACCELERATION,
)
from ocean_science_utilities.wavephysics.balance.generation import (
    WindGeneration,
    TWindInputType,
)
from ocean_science_utilities.wavespectra.operations import integrate_spectral_data
from ocean_science_utilities.wavespectra.spectrum import (
    FrequencyDirectionSpectrum,
    SPECTRAL_DIMS,
)


class SwellDissipation(WindGeneration):
    def __init__(
        self,
        gravitational_acceleration: float = GRAVITATIONAL_ACCELERATION,
        swell_dissipation_coefficients: Optional[Dict[str, float]] = None,
        **kwargs,
    ):
        super(WindGeneration, self).__init__(**kwargs)
        self.gravitational_acceleration = gravitational_acceleration
        if swell_dissipation_coefficients is None:
            swell_dissipation_coefficients = {
                "s0": 3,
                "s1": 0.8,
                "s2": -0.018,
                "s3": 0.015,
                "rz0": 0.04,
                "laminar_coeficient_cds": 1.2,
                "dimensional_critical_reynolds_number": 2e5,
            }
        self.swell_dissipation_coefficients = swell_dissipation_coefficients

    def rate(  # type: ignore
        self,
        spectrum: FrequencyDirectionSpectrum,
        speed: xarray.DataArray,
        direction: xarray.DataArray,
        roughness_length: xarray.DataArray,
        wind_speed_input_type: TWindInputType = "u10",
        air: FluidProperties = AIR,
        water: FluidProperties = WATER,
        memoized: Optional[Dict[str, Any]] = None,
    ) -> xarray.DataArray:
        if wind_speed_input_type == "u10":
            return self.rate_U10(
                speed, direction, spectrum, roughness_length, air, water, memoized
            )

        elif wind_speed_input_type in ["ustar", "friction_velocity"]:
            return self.rate_friction_velocity(
                speed, direction, spectrum, roughness_length, air, water, memoized
            )

        else:
            raise ValueError(
                f"Unknown input type {wind_speed_input_type}, "
                f"has to be one of: 'u10','friction_velocity','ustar'"
            )

    def rate_U10(
        self,
        speed: xarray.DataArray,
        direction: xarray.DataArray,
        spectrum: FrequencyDirectionSpectrum,
        roughness_length: xarray.DataArray,
        air: FluidProperties = AIR,
        water: FluidProperties = WATER,
        memoized: Optional[Dict[str, Any]] = None,
    ) -> xarray.DataArray:
        friction_velocity = (
            air.vonkarman_constant * speed / np.log(10 / roughness_length)
        )
        return self.rate_friction_velocity(
            xarray.DataArray(friction_velocity),
            direction,
            spectrum,
            roughness_length,
            air,
            water,
            memoized,
        )

    def rate_friction_velocity(
        self,
        speed: xarray.DataArray,
        direction: xarray.DataArray,
        spectrum: FrequencyDirectionSpectrum,
        roughness_length: xarray.DataArray,
        air: FluidProperties = AIR,
        water: FluidProperties = WATER,
        memoized: Optional[Dict[str, Any]] = None,
    ) -> xarray.DataArray:
        memoized = memoized if memoized is not None else {}
        if "wave_speed" not in memoized:
            memoized["wave_speed"] = spectrum.wave_speed()

        if "wavenumber" not in memoized:
            memoized["wavenumber"] = spectrum.wavenumber

        if "significant_wave_height" not in memoized:
            memoized["significant_wave_height"] = spectrum.significant_waveheight

        if "significant_orbital_velocity" not in memoized:
            memoized["significant_orbital_velocity"] = st4_significant_orbital_velocity(
                spectrum.variance_density,
                spectrum.radian_frequency,
                memoized["wavenumber"],
                spectrum.depth,
            )

        if "wave_reynolds_number" not in memoized:
            memoized["wave_reynolds_number"] = st4_wave_reynolds_number(
                memoized["significant_orbital_velocity"],
                memoized["significant_wave_height"] / 2,
                air,
            )

        if "mutual_angle" not in memoized:
            memoized["mutual_angle"] = (
                ((spectrum.direction - direction + 180.0) % 360.0 - 180.0) * np.pi / 180
            )

        critical_wave_reynolds_number = st4_crictical_reynolds_number(
            self.swell_dissipation_coefficients, memoized["significant_wave_height"]
        )

        swell_dissipation = st4_swell_dissipation(
            speed,
            memoized["mutual_angle"],
            spectrum.variance_density,
            roughness_length,
            memoized["significant_wave_height"] / 2,
            memoized["wave_reynolds_number"],
            critical_wave_reynolds_number,
            memoized["wavenumber"],
            spectrum.radian_frequency,
            memoized["significant_orbital_velocity"],
            self.swell_dissipation_coefficients,
            self.gravitational_acceleration,
            air,
            water,
        )
        return swell_dissipation


def st4_wave_reynolds_number(
    significant_orbital_velocity: xarray.DataArray,
    significant_amplitude: xarray.DataArray,
    air: FluidProperties = AIR,
) -> xarray.DataArray:
    return (
        4
        * significant_orbital_velocity
        * significant_amplitude
        / air.kinematic_viscosity
    )


def st4_significant_orbital_velocity(
    variance_density: xarray.DataArray,
    radian_frequency: xarray.DataArray,
    wavenumber: xarray.DataArray,
    depth: xarray.DataArray,
) -> xarray.DataArray:
    return xarray.DataArray(
        2
        * np.sqrt(
            integrate_spectral_data(
                variance_density * radian_frequency**2 * np.tanh(wavenumber * depth),
                dims=SPECTRAL_DIMS,
            )
        )
    )


def st4_crictical_reynolds_number(
    swell_dissipation_coefficients: Dict[str, float],
    significant_wave_height: xarray.DataArray,
) -> xarray.DataArray:
    return (
        swell_dissipation_coefficients["dimensional_critical_reynolds_number"]
        / significant_wave_height
    )


def st4_swell_dissipation(
    speed: xarray.DataArray,
    mutual_angle: xarray.DataArray,
    variance_density: xarray.DataArray,
    roughness: xarray.DataArray,
    significant_amplitude: xarray.DataArray,
    wave_reynolds_number: xarray.DataArray,
    critical_reynolds_number: xarray.DataArray,
    wavenumber: xarray.DataArray,
    angular_frequency: xarray.DataArray,
    significant_orbital_velocity: xarray.DataArray,
    swell_dissipation_coefficients: Dict[str, float],
    gravitational_acceleration: float,
    air: FluidProperties = AIR,
    water: FluidProperties = WATER,
) -> xarray.DataArray:
    ratio = air.density / water.density

    criterion = wave_reynolds_number <= critical_reynolds_number
    laminar_coeficient = swell_dissipation_coefficients["laminar_coeficient_cds"]
    laminar = -(
        laminar_coeficient
        * ratio
        * 2
        * wavenumber
        * np.sqrt(2 * angular_frequency * air.kinematic_viscosity)
    )

    swell_dissipation_factor = st4_swell_dissipation_factor(
        speed,
        significant_orbital_velocity,
        roughness,
        significant_amplitude,
        mutual_angle,
        swell_dissipation_coefficients,
        water,
    )

    turbulent = -(
        ratio
        * 16
        * swell_dissipation_factor
        * angular_frequency**2
        * significant_orbital_velocity
        / gravitational_acceleration
    )

    return xarray.where(criterion, laminar, turbulent) * variance_density


def st4_swell_dissipation_factor(
    speed: xarray.DataArray,
    significant_orbital_velocity: xarray.DataArray,
    roughness: xarray.DataArray,
    significant_amplitude: xarray.DataArray,
    mutual_angle: xarray.DataArray,
    swell_dissipation_coefficients: Dict[str, float],
    water: FluidProperties,
) -> xarray.DataArray:
    dissipation_factor_grant_maddsen = st4_dissipation_factor_grant_maddsen(
        roughness, significant_amplitude, swell_dissipation_coefficients, water
    )

    return swell_dissipation_coefficients["s1"] * (
        dissipation_factor_grant_maddsen
        + (
            swell_dissipation_coefficients["s3"]
            + swell_dissipation_coefficients["s2"] * np.cos(mutual_angle)
        )
        * speed
        / significant_orbital_velocity
    )


def st4_dissipation_factor_grant_maddsen(
    roughness: xarray.DataArray,
    significant_amplitude: xarray.DataArray,
    swell_dissipation_coefficients: Dict[str, float],
    water: FluidProperties = WATER,
) -> xarray.DataArray:
    dimensionless_roughness = (
        swell_dissipation_coefficients["rz0"] * roughness / significant_amplitude
    )

    kel = kelvin(2 * np.sqrt(dimensionless_roughness))[1]
    return water.vonkarman_constant**2 / (abs(kel) ** 2 * 2)
