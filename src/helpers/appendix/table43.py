import report_input
from helpers.part_1.figure4 import figure4_helper


def get_table43(geo_code):
    df = figure4_helper(geo_code)
    # df.loc["Total"] = df.sum()
    # df.iat[-1, -1] = 1  # Why are we summing percentages, I have no idea
    df["Cumulative Percentage"] = (df["Cumulative Percentage"]*100).astype(float).round().astype(int).astype(str) + "%"
    df["Number of Dwellings"] = df["Number of Dwellings"].astype(int).astype(str)
    df = df.T
    return df


get_table43(report_input.community_cd)
