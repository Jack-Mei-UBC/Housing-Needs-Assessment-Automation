from helpers.context_helpers import df_to_table_with_label_seperated
from helpers.data_parsing.table_import import comprehensive_2006, comprehensive_2011, comprehensive_2016, \
    comprehensive_2021
from helpers.part_1.figure2 import figure2_helper


def get_table41(cd):
    df = figure2_helper(cd)

    flattened_dfs = {
        2006: comprehensive_2006.xs('total by gender', axis=1, level=0),
        2011: comprehensive_2011.xs('total by gender', axis=1, level=0),
        2016: comprehensive_2016.xs('total by gender', axis=1, level=0),
        2021: comprehensive_2021.xs('total by gender', axis=1, level=0),
    }
    for year in range(2006, 2022, 5):
        labels = flattened_dfs[year].columns
        total = next((value for value in labels if 'total' in value.lower()), None)
        df.at["Total", year] = flattened_dfs[year].at[cd, total]

    df = df.astype(int).astype(str)
    return df


get_table41(3511)