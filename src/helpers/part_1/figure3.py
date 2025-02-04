from typing import List

import pandas as pd
import plotly.graph_objects as go

import report_input
from helpers.data_parsing.table_import import comprehensive_2006, \
    comprehensive_2021, PHM_2006, HART_2006
from helpers.data_parsing.tables import image_locations, table_locations, colors
from helpers.introduction.table2 import get_table2

years = [2006, 2021]
def get_figure3(geo_list: List[int]) -> str:
    title = f"Headship rate by age group, 2006 vs. 2021"
    file_name = "figure3"
    df = figure3_helper(geo_list)
    df.to_csv(table_locations + file_name + ".csv")

    label = get_table2(geo_list)
    for year in years:
        for code in geo_list:
            for index in df.index:
                df.at[index, (year, code, "Headship Rate")] = df.at[index, (year, code, "Households")] / df.at[
                    index, (year, code, "Population")]
    df = df.loc[:,(slice(None), slice(None), "Headship Rate")]
    df.columns = df.columns.droplevel(2)
    fig = go.Figure(
        layout={
            "title": title
        },
    )
    for code in geo_list:
        row = label[label["Geo_Code"] == code]
        for year in years:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df.loc[:, (year, code)],
                name=f'{row.at[row.index[0], "Geography"]} - {year}',
                line={"shape": "spline"},
                marker={"color": colors[year]}
            ))
    fig.update_yaxes(tickformat=".0%", rangemode="tozero")
    fig.update_layout(legend=dict(
        orientation="h",
    ))
    fig.write_image(image_locations + file_name + ".png", width=1000, height=500)
    return file_name + ".png"


def figure3_helper(geo_list: List[int]):
    df = pd.DataFrame(
        index=[f"{x} to {x + 9} years" for x in range(15, 76, 10)] + ["85+ years"],
        columns=pd.MultiIndex.from_product([years, geo_list, ["Households", "Population"]])
    )
    flattened_dfs = {
        2006: comprehensive_2006.xs('total by gender', axis=1, level=0),
        2021: comprehensive_2021.xs('total by gender', axis=1, level=0),
    }
    PHM_2006_85 = HART_2006.loc[:, ("85 years+", "total by tenure", "total by income", "total by CHN")]

    for code in geo_list:
        for i, index in enumerate(df.index):
            # index is 15, when i = 0
            # for under 25
            if i == 0:
                df.at[index, (2006, code, "Households")] = PHM_2006.at[code, "under 25 years"]
                df.at[index, (2006, code, "Population")] = \
                    flattened_dfs[2006].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
                df.at[index, (2021, code, "Households")] = flattened_dfs[2021].loc[code, f'15 to 24 years']
                df.at[index, (2021, code, "Population")] = \
                    flattened_dfs[2021].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
            # for 75-84
            elif i == (len(df.index) - 2):
                df.at[index, (2006, code, "Households")] = PHM_2006.at[code, '75 years+'] - PHM_2006_85.at[code]
                df.at[index, (2006, code, "Population")] = \
                    flattened_dfs[2006].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
                df.at[index, (2021, code, "Households")] = flattened_dfs[2021].loc[code, f'{i + 1}5 to {i + 2}4 years']
                df.at[index, (2021, code, "Population")] = \
                    flattened_dfs[2021].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
            # for 85+
            elif i == (len(df.index) - 1):
                df.at[index, (2006, code, "Households")] = PHM_2006_85.at[code]
                df.at[index, (2006, code, "Population")] = \
                    flattened_dfs[2006].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
                # First instance is Population, second one is PHM
                df.at[index, (2021, code, "Households")] = flattened_dfs[2021].loc[code, '85 years+'].iat[1]
                df.at[index, (2021, code, "Population")] = flattened_dfs[2021].loc[code, '85 years+'].iat[0]
            # for 25-74
            else:
                df.at[index, (2006, code, "Households")] = PHM_2006.at[code, f'{i + 1}5 to {i + 2}4 years']
                df.at[index, (2006, code, "Population")] = \
                    flattened_dfs[2006].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
                df.at[index, (2021, code, "Households")] = flattened_dfs[2021].loc[code, f'{i + 1}5 to {i + 2}4 years']
                df.at[index, (2021, code, "Population")] = \
                    flattened_dfs[2021].loc[code, [f'{i + 1}5 to {i + 1}9 years', f'{i + 2}0 to {i + 2}4 years']].sum()
    return df


get_figure3(report_input.community_csds)
