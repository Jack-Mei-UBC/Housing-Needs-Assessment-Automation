import pandas as pd
import plotly.graph_objects as go

from helpers.data_parsing.table_import import dwelling_type_period_2021
from helpers.data_parsing.tables import image_locations, table_locations, dwelling_colors
from helpers.introduction.table2 import get_table2


def get_figure5(geo_code: int) -> str:
    label = get_table2([geo_code])
    title = f"2021 Housing stock by Dwelling Type, Period of Construction - [{label.at[label.index[0], 'Geography']}]"
    file_name = "figure5"

    # get percentage built
    total = "total by construction period"
    periods = list(dwelling_type_period_2021.columns.levels[0])
    periods.remove(total)
    relevant_housing = [
        'Single-detached house',
        'Apartment in a building that has five or more storeys',
        'Apartment in a building that has fewer than five storeys',
        'Apartment or flat in a duplex',
        'Other single-attached house',
        'Semi-detached house',
        'Row house',
        'Movable dwelling'
    ]
    # Group the dwelling types
    dwelling_data: pd.DataFrame = dwelling_type_period_2021.loc[geo_code, (periods, relevant_housing)].unstack(level=1)
    dwelling_data.loc[:, "Attached, semi-detached, row housing"] = \
        dwelling_data.loc[:, 'Other single-attached house'] \
        + dwelling_data.loc[:, "Semi-detached house"] \
        + dwelling_data.loc[:, "Row house"]
    dwelling_data.loc[:, "Apartment in building with <5 storeys, duplexes"] = \
        dwelling_data.loc[:, "Apartment in a building that has fewer than five storeys"] \
        + dwelling_data.loc[:, "Apartment or flat in a duplex"]

    # Rename the columns
    dwelling_data = dwelling_data.rename(columns={
        'Apartment in a building that has five or more storeys': "Apartment in building with 5+ storeys",
    })
    dwelling_data = dwelling_data.drop(columns=[
        'Other single-attached house',
        'Semi-detached house',
        'Row house',
        "Apartment in a building that has fewer than five storeys",
        "Apartment or flat in a duplex"
    ])

    # Get the percentage built by period
    dwelling_data = dwelling_data.div(dwelling_data.sum(axis=1), axis=0)

    # Create the plotly figure as a horizontal 100 stacked bar chart
    # Each row is a period, with the fraction of housing types built in that period
    # stack the charts for each period
    fig = go.Figure()
    for dwelling_type in dwelling_data.columns:
        fig.add_trace(go.Bar(
            y=dwelling_data.index,
            x=dwelling_data[dwelling_type],
            name=dwelling_type,
            orientation='h',
            marker_color=dwelling_colors[dwelling_type],
        ))

    # Add the title and labels
    # Show proportion axis as percentage
    fig.update_layout(
        title=title,
        xaxis_title="Proportion of all dwellings",
        xaxis_tickformat=".0%",
        yaxis_title="Period of construction",
        barmode="stack",
        legend=dict(
            orientation="h",
        ),

    )

    # Move legend to bottom of plot
    fig.update_layout(
        legend=dict(
            y=-0.2,
        )
    )
    fig.write_image(image_locations + file_name + ".png", width=1000, height=500)
    dwelling_data.to_csv(table_locations + file_name + ".csv")
    return file_name + ".png"

