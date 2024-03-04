import report_input
from helpers.context_helpers import df_to_table_with_label_seperated
from helpers.part_1.figure2 import figure2_helper
from helpers.part_1.figure3 import figure3_helper
from helpers.part_1.part_2_community_names import single_community_name


def get_table42(geo_list):
    df = figure3_helper(geo_list)
    df.loc["Total"] = df.sum()
    df = df.astype(int).astype(str)
    # Change the CD codes to names of regions
    df.columns = df.columns.set_levels([single_community_name(code) for code in df.columns.levels[1]], level=1)
    return df


get_table42(report_input.community_csds)
