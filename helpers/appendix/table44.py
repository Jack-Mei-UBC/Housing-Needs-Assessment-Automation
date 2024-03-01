import report_input
from helpers.part_1.figure5 import figure5_helper


def get_table44(geo_code):
    df = figure5_helper(geo_code)
    df.loc["Total"] = df.sum()
    df = df.astype(int).astype(str)
    df = df.T
    return df


get_table44(report_input.community_cd)
