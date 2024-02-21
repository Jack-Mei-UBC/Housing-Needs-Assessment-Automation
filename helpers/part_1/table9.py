from typing import Dict

import pandas as pd
from helpers.data_parsing.table_import import consolidated_2006, consolidated_2016, consolidated_2021

shelter_cost = [
    "very low shelter cost",
    "low shelter cost",
    "moderate shelter cost",
    "high shelter cost",
    "very high shelter cost"
]


def get_table9(cd: int) -> pd.DataFrame:
    df = pd.DataFrame(
        index=shelter_cost,
        columns=[2016, 2021]
    )

    tables: Dict[int, pd.DataFrame] = {
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    for year in df.columns:
        # Get any total from level 0 of dataframe
        labels = list(tables[year].columns.levels[0])
        total = next((value for value in labels if 'total' in value.lower()), None)
        # All totals do the same damn thing, please only keep one in the future
        data: pd.Series = tables[year].loc[cd, (total, "total by household size", shelter_cost, "total by CHN")]
        data.index = data.index.get_level_values(2)
        df.loc[:, year] = data
    # Add totals
    df.loc["Total", :] = df.sum()
    # Calculate % changes between 2006 and 2016, then 2016 to 2021 as new columns
    df["change"] = (df[2021] - df[2016]) / df[2016] * 100
    # Make populations integers
    percent_start = 2
    df.iloc[:, :percent_start] = df.iloc[:, :percent_start].astype(int)

    # Make percentages actually percent
    df.iloc[:, percent_start:] = (df.iloc[:, percent_start:]).astype(int).astype(str) + "%"
    return df


get_table9(1)
