from typing import Dict

import numpy as np
import pandas as pd
from helpers.data_parsing.table_import import tenure_2016, tenure_2021
from report_input import percent_CHN_by

CHN_status = ["total by CHN", "examined for CHN", "CHN"]
tenureship = ["owner", "with mortgage", "without mortgage", "renter", "subsidized", "unsubsidized"]


def get_table20_23(geo_code: int, year: int) -> pd.DataFrame:
    tables: Dict[int, pd.DataFrame] = {
        2016: tenure_2016,
        2021: tenure_2021
    }
    # Get any total from level 0 of dataframe
    df: pd.DataFrame = tables[year].loc[geo_code, tenureship].unstack()
    # Calculate totals
    df.loc["Total", :] = df.sum()
    # Calulate % CHN by income
    df.loc[:, "% in CHN"] = df.loc[:, "CHN"] / df.loc[:, percent_CHN_by] * 100
    df = df.replace(np.NaN,0)
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
        "owner": "Owner",
        "with mortgage": "With mortgage",
        "without mortgage": "Without mortgage",
        "renter": "Renter",
        "subsidized": "Subsidized",
        "unsubsidized": "Not subsidized"
    }, axis=0)
    return df

