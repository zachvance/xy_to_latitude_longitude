#!/usr/bin/env python3

"""

=======================================================================
X & Y to Latitude & Longitude Coordinate Conversion
=======================================================================

This module takes a CSV file as an input, transforming the specified x
and y coordinate columns into latitude and longitude coordinates. It
will merge the result with the original CSV. It does not require
geopandas to work.

"""

from typing import List

import pandas as pd
from pyproj import Proj, transform

from config import (
    FILE_TO_READ,
    FILE_TO_WRITE,
    IN_PROJ_TYPE,
    LATITUDE_HEADER,
    LONGITUDE_HEADER,
    OUT_PROJ_TYPE,
    RUN_DOCTEST,
    X_HEADER,
    Y_HEADER,
)


def convert_coordinate_pair(x: float, y: float) -> List:
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
    >>> from main import convert_coordinate_pair
    >>> convert_coordinate_pair(643738.9549, 4780141.155)
    [43.16037825643469, -79.23192892861867]
    """

    in_proj = Proj(IN_PROJ_TYPE)
    out_proj = Proj(OUT_PROJ_TYPE)
    x_converted, y_converted = transform(in_proj, out_proj, x, y)
    coordinate_pair = []
    coordinate_pair.append(x_converted)
    coordinate_pair.append(y_converted)
    return coordinate_pair


def convert_dataframe(dataframe: pd.DataFrame) -> List:
    """
    Takes the specified x and y columns from the loaded data frame and
    zips them together before transforming them via the
    convert_coordinate_pair function.

    :param dataframe: A pandas dataframe containing columns of X and Y
    coordinates.
    :type dataframe: pd.DataFrame

    :return: A complete list of all converted coordinate pairs.
    :rtype: list

    Example:
    >>> from main import convert_dataframe
    >>> data = {X_HEADER: [643738.9549], Y_HEADER: [4780141.155]}
    >>> df = pd.DataFrame(data=data)
    >>> convert_dataframe(df)
    [[43.16037825643469, -79.23192892861867]]
    """

    return [
        convert_coordinate_pair(x, y)
        for x, y in zip(dataframe[X_HEADER], dataframe[Y_HEADER])
    ]


def run_tests():
    import doctest

    if RUN_DOCTEST == 1:
        doctest.testmod(verbose=True)
        exit()


def main():
    df = pd.read_csv(FILE_TO_READ)
    latitude_longitude = pd.DataFrame(
        convert_dataframe(df),
        columns=[LATITUDE_HEADER, LONGITUDE_HEADER],
    )
    df = df.join(latitude_longitude)
    df.to_csv(FILE_TO_WRITE, index=False)


if __name__ == "__main__":
    run_tests()
    main()
