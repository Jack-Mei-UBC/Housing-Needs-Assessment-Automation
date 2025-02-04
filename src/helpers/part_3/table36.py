from typing import List

import pandas as pd

from helpers.data_parsing.table_import import consolidated_2021

hh_size_labels = ["1 person", "2 persons", "3 persons", "4 persons", "5+ persons", "total by household size"]


def get_table36(geo_code_list: List[int]):
    df = pd.DataFrame(columns=geo_code_list, index=hh_size_labels)
    for geo_code in geo_code_list:
        df[geo_code] = get_table36_helper(geo_code)
    # Change column names to c0-c3 to make formatting easier
    df = df.rename(
        index={"1 person": "1p.", "2 persons": "2p.", "3 persons": "3p.", "4 persons": "4p.", "5+ persons": "5+ p.",
                "total by household size": "Total"}
    )
    df.columns = [f"c{x}" for x in range(len(geo_code_list))]
    # df.loc["Total"] = df.sum()
    df = df.astype(int)
    return df


def get_table36_helper(geo_code: int):
    labels = list(consolidated_2021.columns.levels[0])
    total_0 = next((value for value in labels if 'total' in value.lower()), None)
    labels = list(consolidated_2021.columns.levels[2])
    total_1 = next((value for value in labels if 'total' in value.lower()), None)
    labels = list(consolidated_2021.columns.levels[3])
    total_2 = next((value for value in labels if 'total' in value.lower()), None)
    row: pd.Series = consolidated_2021.loc[geo_code, (total_0, hh_size_labels, total_1, total_2)]
    row = row.droplevel([0, 2, 3])
    # Change index name to match ours
    # row = row.rename({hh_size_labels[i]: i+1 for i, label in enumerate(hh_size_labels)})
    # Get totals for row and columns
    # row['Total'] = row.sum()
    # Rename columns and rows
    return row


# get_table36([3511015])