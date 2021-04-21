# PyTest file for all preprocessing of data

import io
import builtins
import pytest
import pandas as pd
import sys
import os

# Parent Folder
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)

# Preprocess Python file
import preprocess_data

FILE_NAME = "testWeatherAUS"
DATA_PATH = (
    os.path.dirname(os.path.realpath(__file__)) + "/test_data/" + FILE_NAME + ".csv"
)
PROCESSED_DATA_PATH = (
    os.path.dirname(os.path.realpath(__file__))
    + "/test_data/"
    + FILE_NAME
    + "_processed.csv"
)


def test_count_nulls_by_line():
    # Tests function that counts number of nulls by line on a dataframe
    data = pd.DataFrame([[0, 2], [0, 1], [6, None]])
    assert preprocess_data.count_nulls_by_line(data).to_list() == [1, 0]


def test_null_percent():
    # Tests function that gets the percentage of nulls by line on a dataframe
    data = pd.DataFrame([[0, 2], [1, None]])
    assert preprocess_data.null_percent_by_line(data).to_list() == [0.5, 0]


# @pytest.mark.dependency()
# def test_preprocess():
#     # Checks if running the preprocess function returns an error
#     preprocess_data.preprocess_data(DATA_PATH)


# @pytest.mark.dependency(depends=["test_preprocess"])
# def test_processed_file_created():
#     #  Checks if the processed file was created during test_preprocess() and is accessible
#     f = open(PROCESSED_DATA_PATH)


# @pytest.mark.dependency(depends=["test_processed_file_created"])
# def test_processed_file_format():
#     # Checks if the processed file is in  the correct format (.csv) and can be transformed in dataframe
#     try:
#         pd.read_csv(PROCESSED_DATA_PATH)
#     except:
#         raise RuntimeError("Unable to open " + PROCESSED_DATA_PATH + " as dataframe")


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    # Runs tests then cleans up the processed file
    yield
    try:
        os.remove(PROCESSED_DATA_PATH)
    except:
        pass
