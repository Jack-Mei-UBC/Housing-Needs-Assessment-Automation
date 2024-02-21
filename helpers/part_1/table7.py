from typing import Dict

import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021, consolidated_2006

ownership = ["owner", "renter"]


def get_table7(cd: int) -> pd.DataFrame:
    df = pd.DataFrame(
        index=ownership,
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
        data: pd.Series = tables[year].loc[cd, (total, ownership, "total by income", "total by CHN")]
        data.index = data.index.get_level_values(1)
        df.loc[:, year] = data

    # Calculate % changes between 2006 and 2016, then 2016 to 2021 as new columns
    df.loc["% Owner", :] = df.loc["owner", :] / df.sum(axis=0)*100
    df.loc["% Renter", :] = df.loc["renter", :] / df.sum(axis=0)*100
    # Make populations integers
    slice_loc = 2
    df.iloc[:slice_loc, :] = df.iloc[:slice_loc, :].astype(int)

    # Make percentages actually percent
    df.iloc[slice_loc:, :] = (df.iloc[slice_loc:, :]).astype(int).astype(str) + "%"

    df = df.rename({"owner": "Owner HHs", "renter": "Renter HHs"}, axis=0)
    return df


get_table7(1)
