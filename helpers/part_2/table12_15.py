from typing import Dict

import numpy as np
import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021
from report_input import percent_CHN_by

CHN_status = ["total by CHN", "examined for CHN", "CHN"]
income = ["very low income", "low income", "moderate income", "median income", "high income"]


def get_table12_15(geo_code: int, year: int) -> pd.DataFrame:
    tables: Dict[int, pd.DataFrame] = {
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    # Get any total from level 0 of dataframe
    labels = list(tables[year].columns.levels[0])
    total = next((value for value in labels if 'total' in value.lower()), None)
    # Get raw data
    df = tables[year].loc[geo_code, (total, "total by household size", income, CHN_status)]
    df: pd.DataFrame = df.unstack().reset_index(drop=True, level=[0, 1])
    # Calculate totals
    df.loc["Total", :] = df.sum()
    # Calulate % CHN by income
    df.loc[:, "% in CHN"] = df.loc[:, "CHN"] / df.loc[:, percent_CHN_by] * 100
    df = df.replace(np.NaN, 0)
    # Drop the unneeded columns
    df = df.drop(columns=["total by CHN", "examined for CHN"])
    # Make populations integers
    percent_start = 1
    df = df.astype(int).astype(str)

    # Make percentages actually percent
    df.iloc[:, percent_start:] += "%"

    # Rename index
    df = df.rename({"% in CHN": "pctCHN"}, axis=1)
    df = df.rename({
        "very low income": "Very Low",
        "low income": "Low",
        "moderate income": "Moderate",
        "median income": "Median",
        "high income": "High"
    }, axis=0)
    return df


get_table12_15(1, 2016)
