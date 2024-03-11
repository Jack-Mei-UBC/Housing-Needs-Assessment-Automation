from typing import Dict

import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021
from report_input import percent_CHN_by

CHN_status = ["total by CHN", "examined for CHN", "CHN"]


def get_table11(geo_code: int) -> pd.DataFrame:
    df = pd.DataFrame(
        index=CHN_status,
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
        data: pd.Series = tables[year].loc[geo_code, (total, "total by household size", "total by income", CHN_status)]
        data.index = data.index.get_level_values(3)
        df.loc[:, year] = data
    # Calculate % changes between 2006 and 2016, then 2016 to 2021 as new columns
    df.loc["% of HHs in CHN", :] = df.loc["CHN", :] / df.loc[percent_CHN_by, :]*100

    # Make populations integers
    percent_start = 3
    df.iloc[:percent_start, :] = df.iloc[:percent_start, :].astype(int)

    # Make percentages actually percent
    df.iloc[percent_start:, :] = (df.iloc[percent_start:, :]).astype(float).round().astype(int).astype(str) + "%"

    # Rename index
    df = df.rename({
            "CHN": "HHs in CHN",
            "total by CHN": "Total – Private HHs",
            "examined for CHN": "HHs Examined for CHN"
        },
        axis=0)
    return df


# get_table11(1)
