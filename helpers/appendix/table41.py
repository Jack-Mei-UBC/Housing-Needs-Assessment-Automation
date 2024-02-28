import pandas as pd
import plotly.graph_objects as go

import report_input
from helpers.data_parsing.table_import import comprehensive_2006, comprehensive_2011, comprehensive_2016, \
    comprehensive_2021, PHM_2006, HART_2006
from helpers.data_parsing.tables import image_locations, table_locations
from helpers.introduction.table2 import get_table2


def get_figure3(geo_code: int) -> str:
    age_groups = ["0 to 14 years"] + [f"{x} to {x + 9} years" for x in range(15, 85, 10)] + ["85+ years"]
    stats = ["Households", "Population", "Headship Rate"]
    years = [2006, 2011, 2016, 2021]
    df = pd.DataFrame(
        index=age_groups,
        columns=pd.MultiIndex.from_product([years, stats])
    )

    flattened_dfs = {
        2006: comprehensive_2006.xs('total by gender', axis=1, level=0),
        2011: comprehensive_2011.xs('total by gender', axis=1, level=0),
        2016: comprehensive_2016.xs('total by gender', axis=1, level=0),
        2021: comprehensive_2021.xs('total by gender', axis=1, level=0),
    }

    # Calculate Population
    for year in range(2006, 2022, 5):
        for i, index in enumerate(df.index):
            if index == "0 to 14 years":
                df.at[index, (year, "Population")] = flattened_dfs[year].loc[
                    geo_code, [f'{x} to {x + 4} years' for x in range(0, 14, 5)]].sum()
            elif index == "85+ years":
                if year == 2006:
                    df.at[index, (year, "Population")] = \
                        flattened_dfs[year].loc[
                            geo_code, [f'{x} to {x + 4} years' for x in range(85, 100, 5)] + ['100 years+']].sum()
                else:
                    if year >= 2016:
                        # There are three indices with the same label due to the names being shared by different
                        # selections of data (thumbs down from me)
                        df.at[index, (year, "Population")] = flattened_dfs[year].at[geo_code, '85 years+'].iat[0]
                    else:
                        df.at[index, (year, "Population")] = flattened_dfs[year].at[geo_code, '85 years+']
            else:
                # Scuffed way, but it works.  i or i+1 happens to be equal to the year's first number
                df.at[index, (year, "Population")] = flattened_dfs[year].loc[
                    geo_code, [f'{i}5 to {i}9 years', f'{i + 1}0 to {i + 1}4 years']].sum()

    # Calculate Headship Rate
    for i, index in enumerate(df.index):
        # index is 15, when i = 0
        # for under 25
        if i == 0:
            df.at[index, (2006, code)] = \
                PHM_2006.at[code, "under 25 years"] / \
                flattened_dfs[2006].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
            df.at[index, (2021, code)] = \
                flattened_dfs[2021].loc[code, f'15 to 24 years'] / \
                flattened_dfs[2021].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
        # for 75-84
        elif i == (len(df.index) - 2):
            df.at[index, (2006, code)] = \
                (PHM_2006.at[code, '75 years+'] - PHM_2006_85.at[code]) / \
                flattened_dfs[2006].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
            df.at[index, (2021, code)] = \
                flattened_dfs[2021].loc[code, f'{i + 1}5 to {i + 2}4 years'] / \
                flattened_dfs[2021].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
        # for 85+
        elif i == (len(df.index) - 1):
            df.at[index, (2006, code)] = \
                PHM_2006_85.at[code] / \
                flattened_dfs[2006].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
            # First instance is total population, second one is PHM
            df.at[index, (2021, code)] = \
                flattened_dfs[2021].loc[code, '85 years+'].iat[1] / \
                flattened_dfs[2021].loc[code, '85 years+'].iat[0]
        # for 25-74
        else:
            df.at[index, (2006, code)] = \
                PHM_2006.at[code, f'{i + 1}5 to {i + 2}4 years'] / \
                flattened_dfs[2006].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
            df.at[index, (2021, code)] = \
                flattened_dfs[2021].loc[code, f'{i + 1}5 to {i + 2}4 years'] / \
                flattened_dfs[2021].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()

    df.to_csv(table_locations + file_name + ".csv")




get_figure3(report_input.relevant_geo_codes[0])
