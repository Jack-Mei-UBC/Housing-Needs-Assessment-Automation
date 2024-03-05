from helpers.data_parsing.table_import import comprehensive_2006, comprehensive_2011, comprehensive_2016, \
    comprehensive_2021, PHM_2006
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
            total_pop = next((value for value in labels if 'total' in value.lower()), None)
            labels = labels[::-1]
            total_headship = next((value for value in labels if 'total' in value.lower()), None)
            if year == 2006:
                df.at["Total", (2006, cd, "Households")] = PHM_2006.at[cd, "total by age"]
            else:
                df.at["Total", (2021, cd, "Households")] = flattened_dfs[year].loc[cd, total_headship]
            df.at["Total", (year, cd, "Population")] = flattened_dfs[year].at[cd, total_pop]
    # Change the CD codes to names of regions
    for year in [2006, 2021]:
        for code in geo_list:
            for index in df.index:
                df.at[index, (year, code, "Headship Rate")] = df.at[index, (year, code, "Households")] / df.at[
                    index, (year, code, "Population")]

    df.columns = df.columns.set_levels([single_community_name(code) for code in df.columns.levels[1]], level=1)

    vals = df.loc[:, (slice(None), slice(None), "Headship Rate")].map(lambda x: f"{x:.1%}")
    df.loc[:, (slice(None), slice(None), "Population")] = df.loc[:, (slice(None), slice(None), "Population")].astype(int).astype(str)
    df.loc[:, (slice(None), slice(None), "Households")] = df.loc[:, (slice(None), slice(None), "Households")].astype(int).astype(str)
    df = df.astype(str)

    df.loc[:, (slice(None), slice(None), "Headship Rate")] = vals

    df.reindex(columns=[2006, 2021], level=0)
    return df


get_table42([3511])
