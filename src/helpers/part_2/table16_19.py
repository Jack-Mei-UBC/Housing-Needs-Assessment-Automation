from typing import Dict

import numpy as np
import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021
from report_input import percent_CHN_by

CHN_status = ["total by CHN", "examined for CHN", "CHN"]
hh_size = ["1 person", "2 persons", "3 persons", "4 persons", "5+ persons", "total by household size"]


def get_table16_19(geo_code: int, year: int) -> pd.DataFrame:
    tables: Dict[int, pd.DataFrame] = {
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    # Get any total from level 0 of dataframe
    labels = list(tables[year].columns.levels[0])
    total = next((value for value in labels if 'total' in value.lower()), None)
    # Get raw data
    df = tables[year].loc[geo_code, (total, hh_size, "total by income", CHN_status)]
    df: pd.DataFrame = df.unstack().reset_index(drop=True, level=[0, 2])
    # Calculate totals
    # df.loc["Total", :] = df.sum()
    # Calulate % CHN by income
    df.loc[:, "% in CHN"] = df.loc[:, "CHN"] / df.loc[:, percent_CHN_by] * 100
    df = df.replace(np.NaN, 0)
    # Drop the unneeded columns
    df = df.drop(columns=["total by CHN", "examined for CHN"])
    # Make populations integers
    percent_start = 1
    df.iloc[:, percent_start:] = df.iloc[:, percent_start:].astype(float).round()
    df = df.astype(int).astype(str)

    # Make percentages actually percent
    df.iloc[:, percent_start:] += "%"

    # Rename index
    df = df.rename({"% in CHN": "pctCHN"}, axis=1)
    df = df.rename({
        "1 person": "1 p.",
        "2 persons": "2 p.",
        "3 persons": "3 p.",
        "4 persons": "4 p.",
        "5+ persons": "5p. or more",
        "total by household size": "Total"
    }, axis=0)
    return df


get_table16_19(1, 2016)
