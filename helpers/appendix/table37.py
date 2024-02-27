import pandas as pd
import plotly.graph_objects as go

import report_input
from helpers.data_parsing.table_import import comprehensive_2006, \
    comprehensive_2021, PHM_2006, HART_2006
from helpers.data_parsing.tables import image_locations, table_locations
from helpers.introduction.table2 import get_table2


def get_figure3(geo_code: int) -> str:
    title = f"Headship rate by age group, 2006 vs. 2021"
    file_name = "figure3"
    stats = ["Households", "Population", "Headship Rate"]
    years = [2006, 2021]

    df = pd.DataFrame(
        index=[f"{x} to {x + 9} years" for x in range(15, 76, 10)] + ["85+ years"],
        columns=pd.MultiIndex.from_product([years, stats])
    )
    flattened_dfs = {
        2006: comprehensive_2006.xs('total by gender', axis=1, level=0),
        2021: comprehensive_2021.xs('total by gender', axis=1, level=0),
    }
    PHM_2006_85 = HART_2006.loc[:, ("PHM 85+", "total by ownership", "total by income", "total by CHN")]

    for code in stats:
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




get_figure3(report_input.relevant_geo_codes[0], report_input.relevant_geo_codes[1])
