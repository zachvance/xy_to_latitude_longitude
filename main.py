#!/usr/bin/python

"""

=====================================
X & Y to Latitude & Longitude Coordinate Conversion
=====================================

:Author: Zach Vance, zvance@yourbus.com / zachariah.vance@live.com
:Date: 2021-04-17

This module takes a CSV file as an input, transforming the specified x and y coordinate columns into latitude and
longitude coordinates. It will generate two new CSVs based on the data; one being only the transformed latitude and
longitude columns, and the other being the original CSV with the new columns appended.

Library dependencies:
    - pyproj
    - pandas

"""

import pandas as pd
from pyproj import Proj, transform

df = pd.read_csv("trees.csv", encoding="latin1")
xy_df = pd.DataFrame(columns=["lat", "lon"])
x_list = []
y_list = []
appended_list = []


def convert_coords(x, y):
    """This function takes x and y coordinates as an input, returns those coordinates as latitude and longitude, and
    appends those values to a master list. Adjust the EPSG settings as necessary."""

    in_proj = Proj("epsg:2958")
    out_proj = Proj("epsg:4326")
    x1, y1 = x, y
    x2, y2 = transform(in_proj, out_proj, x1, y1)
    l = []
    l.append(x2)
    l.append(y2)
    appended_list.append(l)
    # Uncomment below if you want to have a visual indication of the transformations being done in the terminal window.
    # print(len(appended_list))


def manage_lists():
    """This function takes the x and y columns from the loaded data frame and zips them together before transforming
    them via the convert_coords function. Adjust the header names to reflect the column names in your data frame."""

    for x in df["X_COORD"]:
        x_list.append(x)

    for y in df["Y_COORD"]:
        y_list.append(y)

    for x, y in zip(x_list, y_list):
        convert_coords(x, y)


latlon = pd.DataFrame(appended_list, columns=["lat", "lon"])
df = df.join(latlon)
latlon.to_csv("latlon.csv")
df.to_csv("final_df.csv")
