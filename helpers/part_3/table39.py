from typing import List

import pandas as pd

import report_input
from helpers.context_helpers import get_community_name
from helpers.data_parsing.tables import projections

income = ["20% or under of area median household income (AMHI)",
          "21% to 50% of AMHI",
          "51% to 80% of AMHI",
          "81% to 120% of AMHI",
          "121% or over of AMHI"]


def get_table39(geo_code_list: List[int]):
    df = pd.DataFrame(columns=geo_code_list, index=income)
    for geo_code in geo_code_list:
        df[geo_code] = get_table39_helper(geo_code)
    # Change column names to c0-c3 to make formatting easier
    df.columns = [f"c{x}" for x in range(len(geo_code_list))]
    # Rename income levels
    df = df.rename(
        index={"20% or under of area median household income (AMHI)": 'Very Low', "21% to 50% of AMHI": 'Low',
               "51% to 80% of AMHI": 'Moderate', "81% to 120% of AMHI": 'Median', "121% or over of AMHI": 'High'}
    )
    df.loc["Total"] = df.sum()
    df = df.astype(int)
    return df


def get_table39_helper(geo_code: int):
    row = projections.loc[geo_code, :]
    series = pd.Series(index=income)
    for ic in income:
        series[ic] = row.loc[f"2031 Projected HH with income {ic}"]
    # Get totals for row and columns
    series['Total'] = series.sum()
    # Rename columns and rows
    return series


get_table39(report_input.geo_code_list + [1])
