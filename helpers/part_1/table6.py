from typing import Dict

import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021, consolidated_2006

hh_size = ["1 person", "2 persons", "3 persons", "4 persons", "5+ persons"]


def get_table6(cd: int) -> pd.DataFrame:
    df = pd.DataFrame(
        index=hh_size,
        columns=[2006, 2016, 2021]
    )

    tables: Dict[int, pd.DataFrame] = {
        2006: consolidated_2006,
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    for year in df.columns:
        # Get any total from level 0 of dataframe
        labels = list(tables[year].columns.levels[0])
        total = next((value for value in labels if 'total' in value.lower()), None)
        # All totals do the same damn thing, please only keep one in the future
        data: pd.Series = tables[year].loc[cd, (total, hh_size, "total by income", "total by CHN")]
        data.index = data.index.get_level_values(1)
        df.loc[:, year] = data

    # Add totals
    df.loc["Total", :] = df.sum()
    # Calculate % changes between 2006 and 2016, then 2016 to 2021 as new columns
    df["change"] = (df[2016] - df[2006]) / df[2006] * 100
    df["change1"] = (df[2021] - df[2016]) / df[2016] * 100
    # Make populations integers
    df.iloc[:, :3] = df.iloc[:, :3].astype(int)

    # Make percentages actually percent
    df.iloc[:, 3:] = (df.iloc[:, 3:]).astype(int).astype(str) + "%"
    return df
get_table6(1)