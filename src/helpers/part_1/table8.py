from typing import Dict

import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021, consolidated_2006

ownership = ["subsidized", "unsubsidized"]


def get_table8(geo_code: int) -> Dict:
    df_examined = pd.DataFrame(
        index=ownership,
        columns=[2016, 2021]
    )
    df_total = pd.DataFrame(
        index=ownership,
        columns=[2016, 2021]
    )

    tables: Dict[int, pd.DataFrame] = {
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    for year in df_total.columns:
        # Get any total from level 0 of dataframe
        labels = list(tables[year].columns.levels[0])
        total = next((value for value in labels if 'total' in value.lower()), None)
        # All totals do the same damn thing, please only keep one in the future
        data: pd.Series = tables[year].loc[geo_code, (total, ownership, "total by income", "examined for CHN")]
        data.index = data.index.get_level_values(1)
        df_examined.loc[:, year] = data

        data: pd.Series = tables[year].loc[geo_code, (total, ownership, "total by income", "total by CHN")]
        data.index = data.index.get_level_values(1)
        df_total.loc[:, year] = data

    # Calculate % changes between 2006 and 2016, then 2016 to 2021 as new columns
    df_examined.loc["% Renters in Subsidized Housing", :] = df_examined.loc["subsidized", :] / df_examined.sum(axis=0)*100
    df_total.loc["% Renters in Subsidized Housing", :] = df_total.loc["subsidized", :] / df_total.sum(axis=0)*100
    # Make populations integers
    slice_loc = 2
    df_examined.iloc[:slice_loc, :] = df_examined.iloc[:slice_loc, :].astype(int).map(lambda x: '{:,}'.format(x))
    df_total.iloc[:slice_loc, :] = df_total.iloc[:slice_loc, :].astype(int).map(lambda x: '{:,}'.format(x))

    # Make percentages actually percent
    df_examined.iloc[slice_loc:, :] = (df_examined.iloc[slice_loc:, :]).astype(float).round().astype(int).astype(str) + "%"
    df_total.iloc[slice_loc:, :] = (df_total.iloc[slice_loc:, :]).astype(float).round().astype(int).astype(str) + "%"

    output = {
        "subsEx2016": df_examined.loc["subsidized", 2016],
        "subsEx2021": df_examined.loc["subsidized", 2021],
        "unsubsEx2016": df_examined.loc["unsubsidized", 2016],
        "unsubsEx2021": df_examined.loc["unsubsidized", 2021],
        "subs2016": df_total.loc["subsidized", 2016],
        "subs2021": df_total.loc["subsidized", 2021],
        "unsubs2016": df_total.loc["unsubsidized", 2016],
        "unsubs2021": df_total.loc["unsubsidized", 2021],
        "pct2016": df_total.loc["% Renters in Subsidized Housing", 2016],
        "pct2021": df_total.loc["% Renters in Subsidized Housing", 2021],
    }
    return output


# get_table8(3511)
