from typing import Dict

import pandas as pd

from helpers.data_parsing.table_import import consolidated_2006, consolidated_2016, consolidated_2021
from helpers.part_1.part_2_community_names import single_community_name


def get_table54_56(geo_list, year):
    df:pd.DataFrame = None
    for geo_code in geo_list:
        if df is None:
            df = table54_helper(geo_code, year)
        else:
            df = pd.concat([df, table54_helper(geo_code, year)], axis=1)

    return df


hh_size = ["1 person", "2 persons", "3 persons", "4 persons", "5+ persons", "total by household size"]


def table54_helper(geo_code, year):
    tables: Dict[int: pd.DataFrame] = {
        2006: consolidated_2006,
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    # Get any total from level 0 of dataframe
    labels = list(tables[year].columns.levels[0])
    total = next((value for value in labels if 'total' in value.lower()), None)
    # All totals do the same damn thing, please only keep one in the future
    df: pd.Series = tables[year].loc[geo_code, (total, hh_size, "total by income", "total by CHN")]
    df.index = df.index.get_level_values(1)
    # rename index
    df = df.rename(index={
        "1 person": "1 p.",
        "2 persons": "2 p.",
        "3 persons": "3 p.",
        "4 persons": "4 p.",
        "5+ persons": "5+ p.",
        "total by household size": "Total"
    })
    # df.loc["Total"] = df.sum()
    df = df.astype(int).astype(str)
    df.name = single_community_name(geo_code)
    return df.to_frame()


# get_table54_56(report_input.community_csds, 2021)
