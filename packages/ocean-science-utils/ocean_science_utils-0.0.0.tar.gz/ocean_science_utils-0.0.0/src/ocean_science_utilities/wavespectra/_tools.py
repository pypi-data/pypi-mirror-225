import numpy as np

from numba import njit   # type: ignore
from scipy.interpolate import CubicSpline   # type: ignore
from typing import Tuple, Optional

from ocean_science_utilities.interpolate.spline import cubic_spline
from ocean_science_utilities.tools.grid import midpoint_rule_step
from ocean_science_utilities.tools.time_integration import (
    integrated_response_factor_spectral_tail,
)


@njit(cache=True)
def _fit(
    x: np.ndarray, y: np.ndarray, power: Optional[int]
) -> Tuple[np.ndarray, np.ndarray]:
    X = x**power
    coef = np.sum(X * y) / np.sum(X * X)
    goodness_of_fit = np.sum((coef * X - y) ** 2)
    return coef, goodness_of_fit


@njit(cache=True)
def tail_fit(
    x: np.ndarray, y: np.ndarray, power: Optional[int]
) -> Tuple[np.ndarray, int]:
    if power is None:
        coef_4, goodness_of_fit_4 = _fit(x, y, -4)
        coef_5, goodness_of_fit_5 = _fit(x, y, -5)
        if goodness_of_fit_5 < goodness_of_fit_4:
            return coef_5, -5
        else:
            return coef_4, -4

    else:
        coef, goodness_of_fit = _fit(x, y, power)
        return coef, power


@njit(cache=True)
def transition_frequency(
    energy_last_resoved_frequency, last_resolved_frequency, integrated_tail
):
    """
    Estimate the transition frequency from a -4 to -5 tail given the last
    resolved frequency and the integrated energy
    in the tail.

    :param energy_last_resoved_frequency:
    :param last_resolved_frequency:
    :param integrated_tail:
    :return:
    """
    return (
        (energy_last_resoved_frequency * last_resolved_frequency**4)
        / (
            4 * energy_last_resoved_frequency * energy_last_resoved_frequency
            - 12 * integrated_tail
        )
    ) ** (1 / 3)


@njit(cache=True)
def numba_fill_zeros_or_nan_in_tail(
    variance_density: np.ndarray,
    frequencies: np.ndarray,
    power: Optional[int] = None,
    zero: float = 0.0,
    points_in_fit: int = 10,
    tail_information: Optional[Tuple[Tuple[int, int], np.ndarray]] = None,
) -> np.ndarray:
    input_shape = variance_density.shape
    number_of_elements = 1
    for value in input_shape[:-1]:
        number_of_elements *= value

    number_of_frequencies = input_shape[-1]
    variance_density = variance_density.reshape((number_of_elements, input_shape[-1]))

    if tail_information is None:
        tail_energy = np.zeros(number_of_elements)
        tail_bounds = (frequencies[-1] + 1, frequencies[-1] + 2)
    else:
        tail_energy = tail_information[1]
        tail_bounds = tail_information[0]

    for ii in range(0, number_of_elements):
        for jj in range(number_of_frequencies - 1, -1, -1):
            if variance_density[ii, jj] > zero:
                # Note, for nan values this is also always false. No need to
                # separately check for that.
                index = jj
                break
        else:
            # no valid value found, we cannot extrapolate. Technically this is
            # not needed as we catch this below as
            # well (since index=number_of_frequencies by default). But to make more
            # explicit that we catch for this
            # scenario I leave it in.
            continue

        if index == number_of_frequencies - 1:
            continue
        elif index < points_in_fit:
            continue

        last_resolved_frequency = frequencies[index]
        last_resolved_energy = variance_density[ii, index]

        if tail_energy[ii] > 0.0:
            trans_freq, starting_energy = _compound_tail(
                last_resolved_frequency,
                last_resolved_energy,
                tail_energy[ii],
                tail_bounds,
            )

            for jj in range(index + 1, number_of_frequencies):
                if frequencies[jj] >= trans_freq:
                    variance_density[ii, jj] = (
                        starting_energy * trans_freq * frequencies[jj] ** -5
                    )
                else:
                    variance_density[ii, jj] = starting_energy * (frequencies[jj]) ** -4

        else:
            coef, fitted_power = tail_fit(
                x=frequencies[index - points_in_fit + 1:index + 1],
                y=variance_density[ii, index - points_in_fit + 1:index + 1],
                power=power,
            )

            for jj in range(index + 1, number_of_frequencies):
                variance_density[ii, jj] = coef * (frequencies[jj]) ** fitted_power

    return np.reshape(variance_density, input_shape)


@njit(cache=True)
def _compound_tail(
    last_resolved_frequency,
    last_resolved_energy,
    raw_tail_energy,
    tail_bounds: Tuple[int, int],
):
    transition_frequencies = np.linspace(tail_bounds[0], tail_bounds[1], 11)

    goodness_of_fit = 0.0
    transition_frequency = transition_frequencies[0]
    starting_energy = 0.0
    for index in range(transition_frequencies.shape[0]):
        tail_energy = raw_tail_energy * integrated_response_factor_spectral_tail(
            -4,
            tail_bounds[0],
            tail_bounds[1],
            2.5,
            transition_frequency=transition_frequencies[index],
        )
        freq_int = 1.0 / 3.0 * (
            tail_bounds[0] ** -3 - transition_frequencies[index] ** -3
        ) + 1.0 / 4.0 * transition_frequencies[index] * (
            transition_frequencies[index] ** -4 - tail_bounds[1] ** -4
        )
        current_starting_energy = tail_energy / freq_int
        current_fit = (
            current_starting_energy * last_resolved_frequency**-4
            - last_resolved_energy
        ) ** 2

        if index == 0:
            goodness_of_fit = (
                current_starting_energy * last_resolved_frequency**-5
                - last_resolved_energy
            ) ** 2
            starting_energy = current_starting_energy
            transition_frequency = transition_frequencies[index]

        else:
            if current_fit < goodness_of_fit:
                goodness_of_fit = current_fit
                starting_energy = current_starting_energy
                transition_frequency = transition_frequencies[index]

    return transition_frequency, starting_energy


def _cdf_interpolate_spline(
    frequency: np.ndarray,
    frequency_spectrum: np.ndarray,
    monotone_interpolation: bool = False,
    frequency_axis: int = -1,
    **kwargs
) -> CubicSpline:
    """
    Interpolate the spectrum using the cdf.

    :param interpolation_frequency: frequencies to estimate the spectrum at.
    :param frequency: Frequencies of the spectrum. Shape = ( nf, )
    :param frequency_spectrum: Frequency Variance density spectrum. Shape = ( np , nf )
    :param interpolating_spline_order: Order of the spline to use in the interpolation
        (max 5 supported by scipy)
    :param positive: Ensure the output is positive (e.g. for A1 or B1 densities output
        need not be strictly positive).
    :return:
    """

    # Calculate the binsize for each of the frequency bins. We assume that the given
    # frequencies represent the center of a bin, and that the bin width at frequency i
    # is determined as the sum of half the up and downwind differences:
    #
    #  frequency_step[i]   =  (frequency_step[i] - frequency_step[i-1])/2 +
    #               (frequency_step[i+1] - frequency_step[i])/2
    #
    # At boundaries we simply take twice the up or downwind difference, e.g.:
    #
    # frequency_step[0] = (frequency_step[1] - frequency_step[0])
    #
    frequency_step = midpoint_rule_step(frequency)
    integration_frequencies = np.concatenate(([0], np.cumsum(frequency_step)))
    integration_frequencies = (
        integration_frequencies - frequency_step[0] / 2 + frequency[0]
    )

    cumsum = np.cumsum(frequency_spectrum * frequency_step, axis=frequency_axis)
    shape = list(cumsum.shape)
    shape[frequency_axis] = 1
    cumsum = np.concatenate((np.zeros(shape), cumsum), axis=-1)

    interpolator = cubic_spline(
        integration_frequencies, cumsum, monotone_interpolation=monotone_interpolation
    )

    return interpolator


def spline_peak_frequency(
    frequency: np.ndarray,
    frequency_spectrum: np.ndarray,
    frequency_axis: int = -1,
    monotone_interpolation: bool = True,
) -> np.ndarray:
    """
    Estimate the peak frequency of the spectrum based on a cubic spline interpolation
    of the partially integrated variance.

    :param frequency: Frequencies of the spectrum. Shape = ( nf, )
    :param frequency_spectrum: Frequency Variance density spectrum. Shape = ( np , nf )
    :return: peak frequencies. Shape = ( np, )
    """
    #

    interpolator = _cdf_interpolate_spline(
        frequency, frequency_spectrum, monotone_interpolation, frequency_axis
    )
    interpolator = interpolator.derivative()
    # Find the maxima of the density function by setting dEdf = 0, and finding the
    # roots of all the splines representing the density function.
    list_of_roots_for_all_spectra = interpolator.derivative().roots()

    if frequency_spectrum.ndim == 1:
        list_of_roots_for_all_spectra = [list_of_roots_for_all_spectra]

    # initialize output memory
    peak_frequency = np.zeros(len(list_of_roots_for_all_spectra))

    # We now have a list in which each entry contains all the roots for that given
    # spectrum. Loop over each spectrum and..
    for index, root in enumerate(list_of_roots_for_all_spectra):
        # ..evaluate density spectrum at those roots.
        values_at_roots = interpolator(root)

        # Because the interpolator returns values at the current roots evaluated at
        # _all_ spectra, we still have to select the values at the spectrum of interest.
        # This implementation is silly, adds computational costs, and can
        # probably be improved. It seems "fast enough" so that I'll punt that to
        # another time.
        if len(list_of_roots_for_all_spectra) > 1:
            values_at_roots = values_at_roots[index, :]

        _root = root[np.isfinite(values_at_roots)]
        values_at_roots = values_at_roots[np.isfinite(values_at_roots)]

        # ... get the root that corresponds to the largest peak.
        index_peak = np.argmax(values_at_roots)
        peak_frequency[index] = _root[index_peak]

    return peak_frequency
