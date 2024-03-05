from typing import List

import pandas as pd

from helpers.data_parsing.tables import projections

hh_size = [1, 2, 3, 4, 5]


def get_table33(geo_code_list: List[int]):
    df = pd.DataFrame(columns=geo_code_list, index=hh_size)
    for geo_code in geo_code_list:
        df[geo_code] = get_table33_helper(geo_code)
    # Change column names to c0-c3 to make formatting easier
    df.columns = [f"c{x}" for x in range(len(geo_code_list))]
    # Rename income levels
    df = df.rename(
        index={1: "1p.", 2: "2p.", 3: "3p.", 4: "4p.", 5: "5+ p."}
    )
    df.loc["Total"] = df.sum()
    df = df.astype(int)
    return df


def get_table33_helper(geo_code: int):
    row = projections.loc[geo_code, :]
    series = pd.Series(index=hh_size)
    for pp in hh_size:
        series[pp] = row.loc[f"2031 Population Delta {pp}pp HH"]
    # Get totals for row and columns
    series['Total'] = series.sum()
    # Rename columns and rows
    return series

