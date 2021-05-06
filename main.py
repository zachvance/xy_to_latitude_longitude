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
)
import pandas as pd
from pyproj import Proj, transform


def convert_coords(x, y):
    """
    Parameters:
        x (int): An X coordinate as a decimal integer
        y (int): A Y coordinate as a decimal integer

    Returns:
        A latitude and longitude pair, in the form of a list

    Example:
    >>> from main import convert_coords
    >>> convert_coords(643738.9549, 4780141.155)
    [43.160369755295726, -79.23192578447924]
    """

    in_proj = Proj(IN_PROJ_TYPE)
    out_proj = Proj(OUT_PROJ_TYPE)
    #x1, y1 = x, y
    x_converted, y_converted = transform(in_proj, out_proj, x, y)
    coordinate_pair = []
    coordinate_pair.append(x_converted)
    coordinate_pair.append(y_converted)
    return coordinate_pair

def manage_lists(dataframe):

    # TODO:
    #   - Add a doctest and rewrite docstring
    #   - Revise list names
    """This function takes the x and y columns from the loaded data
    frame and zips them together before transforming them via the
    convert_coords function. Adjust the header names to reflect the
    column names in your data frame."""

    x_list = []
    y_list = []
    appended_list = []

    for x in dataframe[X_HEADER]:
        x_list.append(x)

    for y in dataframe[Y_HEADER]:
        y_list.append(y)

    for x, y in zip(x_list, y_list):
        appended_list.append(convert_coords(x, y))
        # Uncomment below if you want to have a visual indication of
        # the transformations being done in the terminal window.
        #print(len(appended_list))

    return appended_list

def run_tests():
    import doctest
    if RUN_DOCTEST == 1:
        doctest.testmod(verbose=True)
        exit()

def main():
    df = pd.read_csv(FILE_TO_READ)
    latitude_longitude = pd.DataFrame(manage_lists(df),
                                      columns=[LATITUDE_HEADER,
                                               LONGITUDE_HEADER],
                                      )
    df = df.join(latitude_longitude)
    df.to_csv(FILE_TO_WRITE, index=False)


if __name__ == "__main__":
    run_tests()
    main()