import report_input
from helpers.context_helpers import df_to_table_with_label_seperated
from helpers.part_1.figure2 import figure2_helper
from helpers.part_1.figure3 import figure3_helper


def get_table42(geo_list):
    df = figure3_helper(geo_list)
    df.loc["Total"] = df.sum()
    df = df.astype(int).astype(str)
    return df

get_table42(report_input.geo_code_list)