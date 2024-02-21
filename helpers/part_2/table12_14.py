from typing import Dict

import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021
from report_input import percent_CHN_by

CHN_status = ["total by CHN", "examined for CHN", "CHN"]
income = ["very low income", "low income", "moderate income", "high income", "very high income"]


def get_table12_14(cd: int, year: int) -> pd.DataFrame:
    tables: Dict[int, pd.DataFrame] = {
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    # Get any total from level 0 of dataframe
    labels = list(tables[year].columns.levels[0])
    total = next((value for value in labels if 'total' in value.lower()), None)
    # Get raw data
    df: pd.Series = tables[year].loc[cd, (total, "total by household size", income, CHN_status)]
    df: pd.DataFrame = df.unstack().reset_index(drop=True, level=[0, 1])
    # Calculate totals
    df.loc["Total", :] = df.sum()
    # Calulate % CHN by income
    df.loc[:, "% in CHN"] = df.loc[:, "CHN"] / df.loc[:, percent_CHN_by] * 100
    # Drop the unneeded columns
    df = df.drop(columns=["total by CHN", "examined for CHN"])
    # Make populations integers
    percent_start = 1
    df.iloc[:, :percent_start] = df.iloc[:, :percent_start].astype(int)

    # Make percentages actually percent
    df.iloc[:, percent_start:] = (df.iloc[:, percent_start:]).astype(int).astype(str) + "%"

    # Rename index
    df = df.rename({"CHN": "HHs in CHN"}, axis=0)
    df = df.rename({
        "very low income": "Very Low",
        "low income": "Low",
        "moderate income": "Moderate",
        "high income": "High",
        "very high income": "Very High"
    }, axis=1)
    return df


get_table12_14(1, 2016)
