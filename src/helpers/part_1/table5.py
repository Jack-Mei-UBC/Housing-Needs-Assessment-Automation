from typing import Dict

import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021
incomes = ["very low income", "low income", "moderate income", "median income", "high income", "total by income"]


def get_table5(geo_code: int) -> pd.DataFrame:
    df = pd.DataFrame(
        index=incomes,
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
        data: pd.Series = tables[year].loc[geo_code, (total, "total by household size", incomes, "total by CHN")]
        data.index = data.index.get_level_values(2)
        df.loc[:, year] = data


    df2 = pd.DataFrame(
        index=["Equal to & Under 80% AMHI", "Over 80% AMHI"],
        columns=[2016, 2021, "change"]
    )
    df2.loc["Equal to & Under 80% AMHI", :] = df.loc["very low income":"moderate income", :].sum()
    df2.loc["Over 80% AMHI", :] = df.loc["median income":"high income", :].sum()
    # Add totals
    df2.loc["Total", :] = df.loc["total by income"]
    #
    df2["change"] = (df2[2021] - df2[2016]) / df2[2016] * 100
    # Make populations integers
    df2.iloc[:, :2] = df2.iloc[:, :2].astype(int)

    # Make percentages actually percent
    df2.iloc[:, 2:] = (df2.iloc[:, 2:]).astype(float).round().astype(int).astype(str) + "%"
    return df2


# get_table5(3511)