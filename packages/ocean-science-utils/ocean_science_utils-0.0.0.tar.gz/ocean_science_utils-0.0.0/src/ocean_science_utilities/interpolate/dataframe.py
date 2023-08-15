import pandas as pd
import numpy as np

from ocean_science_utilities.interpolate.general import interpolate_periodic
from ocean_science_utilities.tools.time import to_datetime64


def interpolate_dataframe_time(
    dataframe: pd.DataFrame, new_time: np.ndarray
) -> pd.DataFrame:
    """
    A function to interpolate data in a dataframe. We need this function to be able
    to interpolate wrapped variables (e.g.longitudes and directions).
    """

    output = pd.DataFrame()
    output["time"] = new_time
    columns = list(dataframe.columns)
    old_time = to_datetime64(dataframe["time"].values)  # type: ignore
    new_time = to_datetime64(new_time)  # type: ignore

    for name in columns:
        # name: str
        period = None
        if "direction" in name.lower():
            fp_discont = 360
            fp_period = 360
        else:
            fp_discont = None
            fp_period = None

        if name == "time":
            continue

        # Interpolation does not work on anything other than numeric types. If we have
        # an object - we just ignore it (do not include column in output). Fixes a crash
        # due to the new "processing_source" adding a string to
        # Spotter Api data that descibes where the data was processed.
        if dataframe[name].dtype == np.dtype(object):
            continue

        output[name] = interpolate_periodic(
            old_time.astype("float64"),  # type: ignore
            dataframe[name].values,
            new_time.astype("float64"),  # type: ignore
            x_period=period,
            fp_period=fp_period,
            fp_discont=fp_discont,
        )
    return output
