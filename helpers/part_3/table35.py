from typing import List

import pandas as pd

from helpers.context_helpers import get_community_name
from helpers.data_parsing.tables import projections

hh_size = [1, 2, 3, 4, 5]


def get_table_35(geo_code_list: List[int]):
    df = pd.DataFrame(columns=hh_size, index=geo_code_list)
    for geo_code in geo_code_list:
        df.loc[geo_code] = get_table35_helper(geo_code)


def get_table35_helper(geo_code: int):
    geography = get_community_name(geo_code)
    row = projections.loc[geography, :]
    series = pd.Series(index=hh_size)
    for hh in hh_size:
        series[hh] = row.loc[f"Projected {hh}pp HH"]
    # Get totals for row and columns
    series['Total'] = series.sum()
    # Rename columns and rows
    return series


get_table35_helper(1)
