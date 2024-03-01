import pandas as pd

import report_input
from helpers.data_parsing.table_import import AMHI_2016

info_list = ["AMHI", "very low shelter cost", "low shelter cost", "moderate shelter cost", "median shelter cost", "high shelter cost"]
def get_table48(geo_code):
    df: pd.Series = AMHI_2016.loc[geo_code, info_list]
    # rename index
    df = df.rename(index={
        "very low shelter cost": "Very Low",
        "low shelter cost": "Low",
        "moderate shelter cost": "Moderate",
        "median shelter cost": "Median",
        "high shelter cost": "High"
    })
    df.loc["AMHI"] = int(df.loc["AMHI"])
    df.loc["AMHI"] = "${:,.0f}".format(df.loc["AMHI"])

    return df.to_frame()



get_table48(report_input.community_cd)
