import pandas as pd
import plotly.graph_objects as go

import report_input
from helpers.data_parsing.table_import import comprehensive_2006, comprehensive_2011, comprehensive_2016, \
    comprehensive_2021
from helpers.data_parsing.tables import image_locations, table_locations, colors


def get_figure2(geo_code: int) -> str:
    title = f"Population by Age, 2006-2021 - [{report_input.community_name}]"
    file_name = "figure2"
    df = pd.DataFrame(
        index=["0 to 14 years"] + [f"{x} to {x + 9} years" for x in range(15, 75, 10)] + ["85+ years"],
        columns=[2006, 2011, 2016, 2021]
    )

    flattened_dfs = {
        2006: comprehensive_2006.xs('total by gender', axis=1, level=0),
        2011: comprehensive_2011.xs('total by gender', axis=1, level=0),
        2016: comprehensive_2016.xs('total by gender', axis=1, level=0),
        2021: comprehensive_2021.xs('total by gender', axis=1, level=0),
    }

    for year in range(2006, 2022, 5):
        for i, index in enumerate(df.index):
            if index == "0 to 14 years":
                df.at[index, year] = flattened_dfs[year].loc[
                    geo_code, [f'{x} to {x + 4} years' for x in range(0, 14, 5)]].sum()
            elif index == "85+ years":
                if year == 2006:
                    df.at[index, year] = \
                        flattened_dfs[year].loc[
                            geo_code, [f'{x} to {x + 4} years' for x in range(85, 100, 5)] + ['100 years+']].sum()
                else:
                    if year >= 2016:
                        # There are three indices with the same label due to the names being shared by different
                        # selections of data (thumbs down from me)
                        df.at[index, year] = flattened_dfs[year].at[geo_code, '85 years+'].iat[0]
                    else:
                        df.at[index, year] = flattened_dfs[year].at[geo_code, '85 years+']
            else:
                # Scuffed way, but it works.  i or i+1 happens to be equal to the year's first number
                df.at[index, year] = flattened_dfs[year].loc[
                    geo_code, [f'{i}5 to {i}9 years', f'{i + 1}0 to {i + 1}4 years']].sum()

    df.to_csv(table_locations + file_name + ".csv")
    fig = go.Figure(
        layout={
            "title": title
        },
    )
    for year in range(2006, 2022, 5):
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df.loc[:, year],
            name=str(year),
            line={"shape": "spline"},
            marker={"color": colors[year]}
        ))
    fig.update_yaxes(rangemode="tozero", tickformat=",000")
    fig.write_image(image_locations + file_name + ".png", width=1000, height=500)
    return file_name + ".png"

