import numpy as np
import xarray

from logging import DEBUG, INFO
from typing import Callable, Optional, TypeVar
from dataclasses import dataclass

from ocean_science_utilities.tools.log import logger

_T = TypeVar("_T", np.ndarray, xarray.DataArray)

_iteration_depth = 0


@dataclass()
class Configuration:
    atol: float = 1e-4
    rtol: float = 1e-4
    max_iter: int = 100
    aitken_acceleration: bool = True
    fraction_of_points: float = 1
    error_if_not_converged: bool = False
    numerical_derivative_stepsize: float = 1e-4
    use_numba: bool = True


def _log(msg: str, level: int):
    if _iteration_depth > 1:
        # Sub iterations are set to level debug
        level = DEBUG
    logger.log(level, msg)


def fixed_point_iteration(
    function: Callable[[_T], _T],
    guess: _T,
    bounds=(-np.inf, np.inf),
    configuration: Optional[Configuration] = None,
    caller: Optional[str] = None,
) -> _T:
    """
    Fixed point iteration on a vector function. We want to solve the parallal problem
    x=F(x) where x is a vector. Instead of looping over each problem and solving
    them individualy using e.g. scipy solvers, we gain some efficiency by evaluating
    F in parallel, and doing the iteration ourselves. Only worthwhile if
    F is the expensive part and/or x is large.

    :param function:
    :param guess:
    :param max_iter:
    :param atol:
    :param rtol:
    :param caller:
    :return:
    """

    # Get the current identation level. This is only used for
    # displaying messages in logs.
    global _iteration_depth
    whitespace = _iteration_depth * "\t"
    # Increase identationm level in case of any recursive calling of solvers.
    _iteration_depth += 1

    iterates = [guess, guess, guess]

    if configuration is None:
        configuration = Configuration()

    guess = iterates[2]
    mask_finite_guess_points = np.isfinite(guess)
    number_of_active_points = np.nansum(mask_finite_guess_points)

    where = xarray.where if isinstance(guess, xarray.DataArray) else np.where

    if caller is None:
        caller = "unknown"

    msg = f"{whitespace}Starting solver"
    _log(msg, INFO)

    converged = np.zeros(guess.shape, dtype="bool")
    for current_iteration in range(1, configuration.max_iter + 1):
        # Update iterate
        aitken_step = configuration.aitken_acceleration and current_iteration % 3 == 0
        if aitken_step:
            # Every third step do an aitken acceleration step- if requested
            ratio = (iterates[2] - iterates[1]) / (iterates[1] - iterates[0])
            ratio = where(np.isfinite(ratio) & (ratio != 1.0), ratio, 0.0)
            next_iterate = iterates[2] + ratio / (1.0 - ratio) * (
                iterates[2] - iterates[1]
            )
        else:
            next_iterate = function(iterates[2])

        # Bounds check
        if np.isfinite(bounds[0]):
            next_iterate = where(
                (next_iterate <= bounds[0]),
                (bounds[0] - iterates[2]) * 0.5 + iterates[2],
                next_iterate,
            )

        if np.isfinite(bounds[1]):
            next_iterate = where(
                (next_iterate > bounds[1]),
                (bounds[1] - iterates[2]) * 0.5 + iterates[2],
                next_iterate,
            )

        # Roll the iterates, make the last entry the latest estimate
        iterates.append(iterates.pop(0))
        iterates[2] = next_iterate

        # Convergence check
        absolute_difference = np.abs(iterates[2] - iterates[1])

        scale = np.maximum(np.abs(iterates[1]), configuration.atol)
        relative_difference = absolute_difference / scale
        converged[:] = (absolute_difference < configuration.atol) & (
            relative_difference < configuration.rtol
        )

        max_abs_error = np.nanmax(absolute_difference)
        max_rel_error = np.nanmax(relative_difference)
        percent_converged = np.nansum(converged) / number_of_active_points * 100

        number_of_points_converged = np.nansum(converged)

        msg = (
            f"{whitespace} - Iteration {current_iteration}"
            f"(max {configuration.max_iter}), convergence in"
            f"{percent_converged:.2f} % points"
            f"max abs. errors: {max_abs_error:.2e} (atol: {configuration.atol}), max"
            f"rel. error: {max_rel_error:.2e} (rtol: {configuration.rtol})"
        )
        if number_of_points_converged == number_of_active_points and not aitken_step:
            _log(msg, INFO)
            break

        elif (
            number_of_points_converged
            >= number_of_active_points * configuration.fraction_of_points
        ) and not aitken_step:
            _log(msg, INFO)
            break

        else:
            _log(msg, INFO)

    else:
        msg = f"{whitespace}No convergence after {configuration.max_iter}"
        if configuration.error_if_not_converged:
            raise ValueError(msg)

        else:
            iterates[2][~converged] = np.nan
            _log(msg, INFO)

    # Reduce identation level in logging
    _iteration_depth -= 1
    return iterates[2]
