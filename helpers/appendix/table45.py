import report_input
from helpers.part_1.figure5 import figure5_helper
from helpers.part_1.figure6 import figure6_helper


def get_table45(geo_code):
    df = figure6_helper(geo_code)
    df.loc["Total"] = df.sum()
    df = df.T
    df = df.astype(int).astype(str)
    return df


get_table45(report_input.community_cd)
