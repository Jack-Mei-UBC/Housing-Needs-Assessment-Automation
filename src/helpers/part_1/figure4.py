import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import report_input
from helpers.data_parsing.table_import import dwelling_type_period_2021
from helpers.data_parsing.tables import image_locations, table_locations
from helpers.part_1.part_2_community_names import single_community_name


def get_figure4(geo_code: int) -> str:
    label = single_community_name(geo_code)
    title = f"Housing stock in 2021 by Period of Construction - [{label}]"
    file_name = "figure4"

    df = figure4_helper(geo_code)
    # Rename the " to " to "-\n" to save space, also the or to keep things similar
    df.index = [x.replace(" to ", "-<br>") for x in list(df.index)]
    df.index = [x.replace(" or", " or<br>") for x in list(df.index)]
    df.to_csv(table_locations + file_name + ".csv")

    trace1 = go.Bar(
        x=df.index,
        y=df["Number of Dwellings"],
        name="Number of Dwellings",
        marker=dict(
            color='green'
        )
    )
    # Display each datapoint's percentage on the graph for the secondary y axis
    trace2 = go.Scatter(
        x=df.index,
        y=df["Cumulative Percentage"],
        text=df["Cumulative Percentage"].apply(lambda a: f"{a:.0%}"),
        textposition="top center",
        name="Cumulative Percentage",
        yaxis='y2',
        mode='lines+markers+text',
        marker=dict(
            color='grey'
        )
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Change primary to show number instead of k
    # Change secondary y axis to be formatted percentage
    fig.update_yaxes(tickformat=",.0f")
    fig.update_yaxes(
        tickformat=".0%",
        showgrid=False,
        visible=False,
        secondary_y=True
    )
    fig.add_trace(trace1)
    fig.add_trace(trace2, secondary_y=True)


    fig['layout'].update(title=title, xaxis=dict(
        tickangle=0,
    ))

    # fig.update_yaxes(rangemode="tozero")
    fig.update_layout(legend=dict(
        orientation="h",
    ))
    fig.write_image(image_locations + file_name + ".png", width=1000, height=500)
    return file_name + ".png"


def figure4_helper(geo_code: int) -> pd.DataFrame:
    dwelling_data = dwelling_type_period_2021.xs('total by structural type', axis=1, level=1)
    # get percentage built
    total = "total by construction period"
    periods = list(dwelling_data.columns)
    periods.remove(total)

    percentages = dwelling_data.loc[geo_code, periods] / dwelling_data.at[geo_code, total]
    # I want it to have cumulative percentage
    for index in range(1, len(percentages)):
        percentages.iat[index] = percentages.iat[index] + percentages.iat[index - 1]
    df = pd.concat([dwelling_data.loc[geo_code, periods], percentages], axis=1)
    df.columns = ["Number of Dwellings", "Cumulative Percentage"]

    return df


# get_figure4(report_input.community_cd)