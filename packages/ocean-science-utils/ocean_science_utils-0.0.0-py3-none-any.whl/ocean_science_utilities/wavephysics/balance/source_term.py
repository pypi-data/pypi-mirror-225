import numba  # type: ignore
import numpy as np

from abc import ABC
from typing import Any, Dict, Optional, MutableMapping

from ocean_science_utilities.wavespectra.spectrum import FrequencyDirectionSpectrum


class SourceTerm(ABC):
    def __init__(self, parameters: Optional[Any]):
        self._parameters = (
            parameters if parameters is not None else self.default_parameters()
        )

    @property
    def parameters(self) -> numba.typed.Dict:
        return _numba_parameters(**self._parameters)

    def spectral_grid(
        self, spectrum: FrequencyDirectionSpectrum
    ) -> Dict[str, np.ndarray]:
        return _spectral_grid(
            spectrum.radian_frequency.values,
            spectrum.radian_direction.values,
            spectrum.frequency_step.values,
            spectrum.direction_step.values,
        )

    @staticmethod
    def default_parameters() -> MutableMapping:
        return {}

    @parameters.setter  # type: ignore
    def parameters(self, parameters):
        self._parameters = parameters


@numba.njit()
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
