from typing import Dict

import pandas as pd

import report_input
from helpers.data_parsing.table_import import consolidated_2006, consolidated_2016, consolidated_2021
from helpers.part_1.part_2_community_names import single_community_name


def get_table57_59(geo_list, year):
    df:pd.DataFrame = None
    for geo_code in geo_list:
        if df is None:
            df = table57_helper(geo_code, year)
        else:
            df = pd.concat([df, table57_helper(geo_code, year)], axis=1)

    return df


income = ["very low income", "low income", "moderate income", "median income", "high income"]


def table57_helper(geo_code, year):
    tables: Dict[int: pd.DataFrame] = {
        2006: consolidated_2006,
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    # Get any total from level 0 of dataframe
    labels = list(tables[year].columns.levels[0])
    total = next((value for value in labels if 'total' in value.lower()), None)
    # All totals do the same damn thing, please only keep one in the future
    df: pd.Series = tables[year].loc[geo_code, (total, "total by household size", income, "total by CHN")]
    df.index = df.index.get_level_values(2)
    # rename index
    df = df.rename(index={
        "very low income": "Very Low",
        "low income": "Low",
        "moderate income": "Moderate",
        "median income": "Median",
        "high income": "High"
    })
    df.loc["Total"] = df.sum()
    df = df.astype(int).astype(str)
    df.name = single_community_name(geo_code)
    return df.to_frame()


get_table57_59(report_input.community_csds, 2006)
