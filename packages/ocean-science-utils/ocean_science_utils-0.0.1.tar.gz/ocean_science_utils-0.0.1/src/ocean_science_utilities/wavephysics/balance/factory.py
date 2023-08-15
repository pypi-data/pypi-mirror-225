from typing import Dict, Literal

from ocean_science_utilities.wavephysics.balance.balance import SourceTermBalance
from ocean_science_utilities.wavephysics.balance.dissipation import Dissipation
from ocean_science_utilities.wavephysics.balance.jb23_wind_input import JB23WindInput
from ocean_science_utilities.wavephysics.balance.st4_wave_breaking import (
    ST4WaveBreaking,
)
from ocean_science_utilities.wavephysics.balance.st4_wind_input import ST4WindInput
from ocean_science_utilities.wavephysics.balance.st6_wave_breaking import (
    ST6WaveBreaking,
)
from ocean_science_utilities.wavephysics.balance.st6_wind_input import ST6WindInput
from ocean_science_utilities.wavephysics.balance.romero_wave_breaking import (
    RomeroWaveBreaking,
)

breaking_parametrization = Literal["st6", "st4", "romero"]


def create_breaking_dissipation(
    breaking_parametrization: breaking_parametrization = "st6", **kwargs
) -> Dissipation:
    if breaking_parametrization == "st6":
        return ST6WaveBreaking(**kwargs)
    elif breaking_parametrization == "st4":
        return ST4WaveBreaking(**kwargs)
    elif breaking_parametrization == "romero":
        return RomeroWaveBreaking(**kwargs)
    else:
        raise ValueError(f"Unknown parametrization {breaking_parametrization}")


wind_parametrizations = Literal["st6", "st4", "jb23"]


def create_wind_source_term(
    wind_parametrization: wind_parametrizations = "st4", **kwargs
):
    if wind_parametrization == "st6":
        return ST6WindInput(**kwargs)
    elif wind_parametrization == "st4":
        return ST4WindInput(**kwargs)
    elif wind_parametrization == "jb23":
        return JB23WindInput(**kwargs)
    else:
        raise ValueError(f"Unknown parametrization: {wind_parametrization}")


def create_balance(
    generation_par: wind_parametrizations = "st4",
    dissipation_par: breaking_parametrization = "st4",
    generation_args: Dict = {},
    dissipation_args: Dict = {},
) -> SourceTermBalance:
    return SourceTermBalance(
        generation=create_wind_source_term(generation_par, **generation_args),
        disspipation=create_breaking_dissipation(dissipation_par, **dissipation_args),
    )
