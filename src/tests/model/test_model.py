# PyTest file for model.py

import sys
import os
import pytest
import pandas as pd

# Parent Folder
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)

# Model Python file
from model import get_variables

FILE_NAME = "testWeatherAUS"
PROCESSED_DATA_PATH = (
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    + "/test_data/"
    + FILE_NAME
    + "_processed.csv"
)


@pytest.mark.parametrize(
    "expected_X,expected_y",
    [
        (
            {
                "MinTemp": {0: 13.4, 1: 7.4},
                "MaxTemp": {0: 22.9, 1: 25.1},
                "Rainfall": {0: 0.6, 1: 0.0},
                "WindGustSpeed": {0: 44, 1: 44},
                "WindSpeed9am": {0: 20, 1: 4},
                "WindSpeed3pm": {0: 24, 1: 22},
                "Humidity9am": {0: 71, 1: 44},
                "Humidity3pm": {0: 22, 1: 25},
                "Pressure9am": {0: 1007.7, 1: 1010.6},
                "Pressure3pm": {0: 1007.1, 1: 1007.8},
                "Temp9am": {0: 16.9, 1: 17.2},
                "Temp3pm": {0: 21.8, 1: 24.3},
                "RainToday": {0: 0, 1: 0},
                "WindGustDir_W": {0: 1, 1: 0},
                "WindGustDir_WNW": {0: 0, 1: 1},
                "WindDir9am_NNW": {0: 0, 1: 1},
                "WindDir9am_W": {0: 1, 1: 0},
                "WindDir3pm_WNW": {0: 1, 1: 0},
                "WindDir3pm_WSW": {0: 0, 1: 1},
            },
            [0, 0],
        )
    ],
)
def test_get_variables(expected_X, expected_y):

    # Open CSV as DF
    data = pd.read_csv(PROCESSED_DATA_PATH)

    # Run Function
    X, y = get_variables(data, "RainTomorrow")

    assert (X.to_dict(), y.to_list()) == (expected_X, expected_y)
