import pandas as pd

import report_input
from helpers.data_parsing.table_import import AMHI_2021
from helpers.part_1.part_2_community_names import single_community_name

info_list = ["AMHI", "very low shelter cost", "low shelter cost", "moderate shelter cost", "median shelter cost",
             "high shelter cost"]


def get_table52(geo_code):
    df: pd.Series = AMHI_2021.loc[geo_code, info_list]
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

    df.name = single_community_name(geo_code)
    return df.to_frame()


get_table52(report_input.community_cd)
