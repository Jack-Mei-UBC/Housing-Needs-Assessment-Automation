from typing import Dict

import numpy as np
import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021
from report_input import percent_CHN_by

CHN_status = ["total by CHN", "examined for CHN", "CHN"]
pp = ["disabled", "health issues", "aboriginal", "visible minority", "female PHM", "black", "recent immigrant",
      "refugee immigrant", "single mom", "under 24", "65 years+", "85 years+"]


def get_table24_27(geo_code: int, year: int) -> pd.DataFrame:
    tables: Dict[int, pd.DataFrame] = {
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    # Get any total from level 0 of dataframe
    labels = list(tables[year].columns.levels[2])
    total = next((value for value in labels if 'total' in value.lower()), None)
    # Get total for priority population
    labels = list(tables[year].columns.levels[0])
    pp_total = next((value for value in labels if 'total' in value.lower()), None)
    # Get raw data
    df = tables[year].loc[geo_code, (pp + [pp_total], "total by household size", total, CHN_status)]
    df: pd.DataFrame = df.unstack().reset_index(drop=True, level=[1, 2])
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
        "disabled": "HH with physical activity limitation",
        "health issues": "HH with cognitive, mental, or addictions activity limitation",
        "aboriginal": "Indigenous HH",
        "visible minority": "Visible minority HH",
        "female PHM": "Woman-led",
        "black": "Black-led HH",
        "recent immigrant": "New migrant-led HH",
        "refugee immigrant": "Refugee claimant-led HH",
        "single mom": "Single mother-led HH",
        "under 24": "HH head under 24",
        "65 years+": "HH head over 65",
        "85 years+": "HH head over 85",
        pp_total: "Total",
    }, axis=0)
    return df


get_table24_27(3511, 2016)