import numpy as np
from typing import Literal, Optional, Tuple, Union

from ocean_science_utilities.wavespectra.spectrum import (
    FrequencySpectrum,
    FrequencyDirectionSpectrum,
    WaveSpectrum,
)


def surface_timeseries(
    component: Literal["u", "v", "w", "x", "y", "z"],
    sampling_frequency: float,
    signal_length: int,
    spectrum: WaveSpectrum,
    seed: Optional[int] = None,
) -> Tuple[np.typing.NDArray, np.typing.NDArray]:
    """
    Create a timeseries for from a given power spectral density.

    :param component: Wave component to create a timeseries for: u,v,w,x,y,z.
    :param sampling_frequency: Sampling frequency of output signal in Hertz
    :param signal_length: Length of output signal
    :param spectrum: Input power spectrum
    :param seed: Input seed for the random number generator.
    :return:
    """

    nfft = (int(signal_length) // 2) * 2

    frequencies = np.linspace(0, 0.5 * sampling_frequency, nfft // 2, endpoint=False)

    time = np.linspace(0, nfft / sampling_frequency, nfft, endpoint=False)

    timeseries = nfft * np.fft.irfft(
        create_fourier_amplitudes(component, spectrum, frequencies, seed)
    )

    return time, timeseries


def create_fourier_amplitudes(
    component, spectrum: WaveSpectrum, frequencies, seed=None
):
    spectrum = spectrum.interpolate_frequency(frequencies)

    if isinstance(spectrum, FrequencySpectrum):
        radian_directions: Union[float, np.ndarray] = 0.0
        radian_frequency = spectrum.radian_frequency.values
        area = spectrum.frequency_step.values

    elif isinstance(spectrum, FrequencyDirectionSpectrum):
        radian_directions = spectrum.radian_direction.values[None, :]
        radian_frequency = spectrum.radian_frequency.values[:, None]
        area = (
            spectrum.frequency_step.values[:, None]
            * spectrum.direction_step.values[None, :]
        )
    else:
        raise ValueError("Not a spectrum")

    if component == "w":
        factor: Union[float, np.ndarray] = 1j * radian_frequency

    elif component == "u":
        factor = radian_frequency * np.cos(radian_directions)

    elif component == "v":
        factor = radian_frequency * np.sin(radian_directions)

    elif component == "x":
        factor = -1j * np.cos(radian_directions)

    elif component == "y":
        factor = -1j * np.sin(radian_directions)

    else:
        factor = 1.0

    phases = np.random.default_rng(seed=seed).uniform(
        0, 2 * np.pi, spectrum.spectral_shape()
    )
    amplitudes = (
        np.sqrt(area * spectrum.variance_density / 2) * np.exp(1j * phases) * factor
    )

    if isinstance(spectrum, FrequencyDirectionSpectrum):
        amplitudes = np.sum(amplitudes, axis=-1)

    return amplitudes
