#!/usr/bin/env python3

"""

========================================================================
X & Y to Latitude & Longitude Coordinate Conversion
========================================================================

This module takes a CSV file as an input, transforming the specified x
and y coordinate columns into latitude and longitude coordinates. It
will merge the result with the original CSV. It does not require
geopandas to work.

TODO:
    - Rewrite functions so as not to iterate over a pandas data frame
    - Rewrite docstrings after updates
    - Review function names
    - Rewrite docstring in manage_lists function
    - Revise list names in manage_lists function
    - Fix iteration of pandas data frames in manage_lists function

"""

from config import (
    FILE_TO_READ,
    X_HEADER,
    Y_HEADER,
    IN_PROJ_TYPE,
    OUT_PROJ_TYPE,
    LATITUDE_HEADER,
    LONGITUDE_HEADER,
    FILE_TO_WRITE,
    RUN_DOCTEST,
    OUTPUT_TO_CONSOLE,
)
import pandas as pd
from pyproj import Proj, transform
from typing import List

def convert_coordinates(x: float, y: float) -> List:
    """
    Takes an x and y coordinate pair as arguments, and converts them
    into a latitude and longitude coordinate pair via pyproj's
    transform function.

    :param x: An X coordinate as a decimal number.
    :type x: float
    :param y: A Y coordinate as a decimal number.
    :type y: float

    :return: A latitude and longitude pair, in the form of a list.
    :rtype: list

    Example:
    >>> from main import convert_coordinates
    >>> convert_coordinates(643738.9549, 4780141.155)
    [43.16037825643469, -79.23192892861867]
    """

    in_proj = Proj(IN_PROJ_TYPE)
    out_proj = Proj(OUT_PROJ_TYPE)
    x_converted, y_converted = transform(in_proj, out_proj, x, y)
    coordinate_pair = []
    coordinate_pair.append(x_converted)
    coordinate_pair.append(y_converted)
    return coordinate_pair


def manage_lists(dataframe: pd.DataFrame) -> List:
    """
    Old docstring: This function takes the x and y columns from the
    loaded data frame and zips them together before transforming them
    via the convert_coordinates function.

    :param dataframe: A pandas dataframe containing columns of X and Y
    coordinates.
    :type dataframe: pd.DataFrame

    :return: A complete list of all converted coordinate pairs.
    :rtype: list

    Example:
    >>> from main import manage_lists
    >>> data = {X_HEADER: [643738.9549], Y_HEADER: [4780141.155]}
    >>> df = pd.DataFrame(data=data)
    >>> manage_lists(df)
    [[43.16037825643469, -79.23192892861867]]
    """

    x_list = []
    y_list = []
    appended_list = []

    for x in dataframe[X_HEADER]:
        x_list.append(x)

    for y in dataframe[Y_HEADER]:
        y_list.append(y)

    for x, y in zip(x_list, y_list):
        appended_list.append(convert_coordinates(x, y))
        if OUTPUT_TO_CONSOLE == 1:
            print(len(appended_list))

    return appended_list


def run_tests():
    import doctest

    if RUN_DOCTEST == 1:
        doctest.testmod(verbose=True)
        exit()


def main():
    df = pd.read_csv(FILE_TO_READ)
    latitude_longitude = pd.DataFrame(
        manage_lists(df),
        columns=[LATITUDE_HEADER, LONGITUDE_HEADER],
    )
    df = df.join(latitude_longitude)
    df.to_csv(FILE_TO_WRITE, index=False)


if __name__ == "__main__":
    run_tests()
    main()
