import pandas as pd

import report_input
from helpers.data_parsing.table_import import AMHI_2021

info_list = ["AMHI", "very low income", "low income", "moderate income", "median income", "high income"]
def get_table50(geo_code):
    df: pd.Series = AMHI_2021.loc[geo_code, info_list]
    # rename index
    df = df.rename(index={
        "very low income": "Very Low",
        "low income": "Low",
        "moderate income": "Moderate",
        "median income": "Median",
        "high income": "High"
    })
    df.loc["AMHI"] = int(df.loc["AMHI"])
    df.loc["AMHI"] = "${:,.0f}".format(df.loc["AMHI"])

    return df.to_frame()



get_table50(report_input.community_cd)
