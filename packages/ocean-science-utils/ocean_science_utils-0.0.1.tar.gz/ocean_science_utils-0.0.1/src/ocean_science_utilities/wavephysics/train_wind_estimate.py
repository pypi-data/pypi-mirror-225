import numpy as np
import xarray

from typing import List, Optional
from scipy.optimize import minimize  # type: ignore

from ocean_science_utilities.wavephysics.balance.balance import SourceTermBalance
from ocean_science_utilities.wavephysics.balance.wind_inversion import (
    windspeed_and_direction_from_spectra,
)
from ocean_science_utilities.wavespectra.spectrum import (
    FrequencySpectrum,
    FrequencyDirectionSpectrum,
    WaveSpectrum,
)
from ocean_science_utilities.wavephysics.windestimate import estimate_u10_from_spectrum


def rmse(target, actual, jacobian_actual=None, weights=None):
    N = len(target)
    if weights is None:
        weights = 1 / N

    mean_error = sum(weights * (actual - target) ** 2) / 2

    if jacobian_actual is not None:
        error_gradient = (weights * (actual - target))[None, :] @ jacobian_actual
        return mean_error, np.squeeze(error_gradient)
    else:
        return mean_error


def mae(target, actual, jacobian_actual=None, weights=None):
    N = len(target)
    error = sum(np.abs(actual - target)) / N

    if jacobian_actual is not None:
        error_gradient = (np.sign(actual - target)[None, :] @ jacobian_actual) / N
        return error, np.squeeze(error_gradient)
    else:
        return error


def create_weighted_metric(name, binsize, number_of_bins, target):
    bins = np.linspace(0, number_of_bins * binsize, number_of_bins, endpoint=False)
    index = np.digitize(target, bins)
    weights = np.zeros(len(target))
    for ii in range(number_of_bins + 1):
        mask = ii == index
        n = np.sum(mask)

        if n == 0:
            continue

        weights[mask] = 1 / (n * number_of_bins)

    return create_metric(name, weights)


def create_metric(name, weights=None):
    if name == "rmse":
        func = rmse
    elif name == "mae":
        func = mae
    elif name == "huber":
        func = huber

    def _closure(target, actual, jacobian_actual=None):
        return func(target, actual, jacobian_actual, weights=weights)

    return _closure


def huber(target, actual, jacobian_actual=None, weights=None):
    diff = actual - target
    delta = np.abs(diff)
    N = len(target)
    error = sum(np.where(delta < 1, delta**2 / 2, delta - 1 / 2)) / N

    if jacobian_actual is not None:
        vector = np.where(delta < 1, diff, np.sign(diff))
        error_gradient = (vector @ jacobian_actual) / N
        return error, np.squeeze(error_gradient)
    else:
        return error


def calibrate_wind_estimate_from_spectrum(
    method,
    target_u10: xarray.DataArray,
    spectrum: FrequencySpectrum,
    parameter_names: Optional[List[str]] = None,
    loss_function=None,
    velocity_scale=None,
    bounds=None,
    params=None,
):
    if parameter_names is None:
        parameter_names = [
            "phillips_constant_beta",
            "charnock_constant",
        ]

    estimate_default_parameters = {
        "directional_spreading_constant": 2.5,
        "phillips_constant_beta": 0.012,
        "charnock_constant": 0.015,
    }

    scale = {}

    for parameter_name in parameter_names:
        scale[parameter_name] = estimate_default_parameters[parameter_name]

    if loss_function is None:
        loss_function = rmse

    if velocity_scale is None:
        velocity_scale = np.median(target_u10)

    if params is None:
        params = {}

    x0 = np.ones(len(parameter_names))

    def training_function(values):
        estimate_input = {}
        for parameter_name, value in zip(parameter_names, values):
            estimate_input[parameter_name] = value * scale[parameter_name]

        estimate_input = estimate_default_parameters | estimate_input | params

        estimate = estimate_u10_from_spectrum(spectrum, method=method, **estimate_input)

        actual = estimate["u10"].values / velocity_scale
        actual[np.isnan(actual)] = 0.0
        target = target_u10.values / velocity_scale
        return loss_function(target, actual)

    if bounds is None:
        _bounds = [(0.01, 100) for x in x0]
    else:
        _bounds = []
        for parameter_name in parameter_names:
            x = bounds[parameter_name]
            _scale = scale[parameter_name]
            _bounds.append((x[0] / _scale, x[1] / _scale))

    options = {"maxiter": 100, "disp": True}

    res = minimize(
        training_function, x0, method="SLSQP", bounds=_bounds, options=options
    )

    return {key: x * scale[key] for key, x in zip(parameter_names, res.x)}


def calibrate_wind_estimate_from_balance(
    balance: SourceTermBalance,
    parameter_names: List[str],
    target_u10: xarray.DataArray,
    spectrum: FrequencyDirectionSpectrum,
    loss_function=None,
    velocity_scale=None,
    params=None,
    time_derivative_spectrum: Optional[FrequencyDirectionSpectrum] = None,
    direction_iteration=False,
):
    dissipation = balance.dissipation
    generation = balance.generation

    if params is not None:
        balance.update_parameters(params)

    scale = {}
    for parameter_name in parameter_names:
        if parameter_name in dissipation._parameters:
            par = dissipation._parameters
        elif parameter_name in generation._parameters:
            par = generation._parameters
        else:
            raise ValueError(f"unknown parameter {parameter_name}")
        scale[parameter_name] = par[parameter_name]

    if loss_function is None:
        loss_function = rmse

    if velocity_scale is None:
        velocity_scale = np.median(target_u10)

    def training_function(values):
        """
        Training function that returns the current loss value.
        :param values: list of scaled floats, in the order of the names in
            parameter names
        :return: the loss function and an approximation of the gradient
        """
        params = {}
        for parameter_name, value in zip(parameter_names, values):
            params[parameter_name] = value * scale[parameter_name]

        balance.update_parameters(params)

        # Estimate the wind speed, direction and gradient.
        estimate = windspeed_and_direction_from_spectra(
            balance,
            target_u10,
            spectrum,
            jacobian=True,
            jacobian_parameters=parameter_names,
            time_derivative_spectrum=time_derivative_spectrum,
            direction_iteration=direction_iteration,
        )
        actual = estimate["u10"].values
        actual[~np.isfinite(actual)] = 0.0
        actual = estimate["u10"].values / velocity_scale
        actual[np.isnan(actual)] = 0.0

        target = target_u10.values / velocity_scale

        jacobian = estimate["jacobian"].values / velocity_scale

        err, grad_err = loss_function(target, actual, jacobian_actual=jacobian)

        # Apply scaling
        for index, parameter_name in enumerate(parameter_names):
            grad_err[index] = grad_err[index] * scale[parameter_name]

        return (err, grad_err)

    x0 = np.ones(len(parameter_names))
    bounds = [(0.01, 100) for x in x0]
    options = {"maxiter": 100, "disp": True}

    res = minimize(
        training_function,
        x0,
        method="SLSQP",
        bounds=bounds,
        options=options,
        jac=True,
    )

    return balance.get_parameters | {
        key: x * scale[key] for key, x in zip(parameter_names, res.x)
    }


def prep_data(
    spectrum: WaveSpectrum, target_u10: xarray.DataArray, threshold=(-np.inf, np.inf)
):
    mask = (
        (spectrum.is_valid())
        & (target_u10.values >= threshold[0])
        & (target_u10.values <= threshold[1])
    )

    return spectrum.where(mask), target_u10[mask.values]
