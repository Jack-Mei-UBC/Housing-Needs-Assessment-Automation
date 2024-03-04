from typing import List

import pandas as pd

import report_input
from helpers.data_parsing.table_import import consolidated_2021

income_labels = ["very low income", "low income", "moderate income", "median income", "high income"]


def get_table40(geo_code_list: List[int]):
    df = pd.DataFrame(columns=geo_code_list, index=income_labels)
    for geo_code in geo_code_list:
        df[geo_code] = get_table40_helper(geo_code)
    # Change column names to c0-c3 to make formatting easier
    df.columns = [f"c{x}" for x in range(len(geo_code_list))]
    df = df.rename(
        index={"very low income": "Very Low", "low income": "Low", "moderate income": "Moderate",
               "median income": "Median", "high income": "High"}
    )
    df.loc["Total"] = df.sum()
    df = df.astype(int)
    return df


def get_table40_helper(geo_code: int):
    labels = list(consolidated_2021.columns.levels[0])
    total_0 = next((value for value in labels if 'total' in value.lower()), None)
    labels = list(consolidated_2021.columns.levels[1])
    total_1 = next((value for value in labels if 'total' in value.lower()), None)
    labels = list(consolidated_2021.columns.levels[3])
    total_2 = next((value for value in labels if 'total' in value.lower()), None)
    row: pd.Series = consolidated_2021.loc[geo_code, (total_0, total_1, income_labels, total_2)]
    row = row.droplevel([0, 1, 3])
    # Get totals for row and columns
    row['Total'] = row.sum()
    # Rename columns and rows
    return row


get_table40(report_input.community_csds)
