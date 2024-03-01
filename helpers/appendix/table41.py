from helpers.context_helpers import df_to_table_with_label_seperated
from helpers.part_1.figure2 import figure2_helper


def get_table41(cd):
    df = figure2_helper(cd)
    df.loc["Total"] = df.sum()
    df = df.astype(int).astype(str)
    return df
