import report_input
from helpers.context_helpers import df_to_table_with_label_seperated
from helpers.data_parsing.table_import import comprehensive_2006, comprehensive_2011, comprehensive_2016, \
    comprehensive_2021, PHM_2006
from helpers.part_1.figure2 import figure2_helper
from helpers.part_1.figure3 import figure3_helper
from helpers.part_1.part_2_community_names import single_community_name


def get_table42(geo_list):
    df = figure3_helper(geo_list)

    flattened_dfs = {
        2006: comprehensive_2006.xs('total by gender', axis=1, level=0),
        2011: comprehensive_2011.xs('total by gender', axis=1, level=0),
        2016: comprehensive_2016.xs('total by gender', axis=1, level=0),
        2021: comprehensive_2021.xs('total by gender', axis=1, level=0),
    }
    for cd in geo_list:
        for year in [2006, 2021]:
            labels = flattened_dfs[year].columns
            total = next((value for value in labels if 'total' in value.lower()), None)
            if year == 2006:
                df.at["Total", (2006, cd, "Headship Population")] = PHM_2006.at[cd, "total by age"]
            else:
                df.at["Total", (2021, cd, "Headship Population")] = flattened_dfs[year].loc[cd, total]
            df.at["Total", (year, cd, "Total Population")] = flattened_dfs[year].at[cd, total]
    df = df.astype(int).astype(str)
    # Change the CD codes to names of regions
    df.columns = df.columns.set_levels([single_community_name(code) for code in df.columns.levels[1]], level=1)
    return df


get_table42(report_input.community_csds)
