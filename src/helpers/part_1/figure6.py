import pandas as pd
import plotly.graph_objects as go

from helpers.data_parsing.table_import import dwelling_type_bedrooms_2021
from helpers.data_parsing.tables import image_locations, table_locations, bedroom_colors
from helpers.introduction.table2 import get_table2


def get_figure6(geo_code: int) -> str:
    label = get_table2([geo_code])
    title = f"2021 Housing stock by Number of Bedrooms, Dwelling Type - [{label.at[label.index[0], 'Geography']}]"
    file_name = "figure6"

    dwelling_data = figure6_helper(geo_code)

    fig = go.Figure()
    for bedroom_count in dwelling_data.index:
        fig.add_trace(go.Bar(
            y=dwelling_data.columns,
            x=dwelling_data.loc[bedroom_count, :],
            name=bedroom_count,
            orientation='h',
            marker_color=bedroom_colors[bedroom_count],
        ))

    # Add the title and labels
    # Show proportion axis as percentage
    fig.update_layout(
        title=title,
        xaxis_title="Number of Dwellings by bedroom count",
        barmode="stack",
        legend=dict(
            orientation="h",
        ),

    )
    fig.update_xaxes(
        tickformat=",.0f",
    )

    # Move legend to bottom of plot
    fig.update_layout(
        legend=dict(
            y=-0.2,
            # orientation="h",
            # entrywidthmode='fraction',
            # entrywidth=1.5,
        )
    )
    fig.write_image(image_locations + file_name + ".png", width=1000, height=500)
    dwelling_data.to_csv(table_locations + file_name + ".csv")
    return file_name + ".png"


def figure6_helper(geo_code: int) -> pd.DataFrame:
    # get percentage built
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
    # Query dwelling data by relevant housing types multiindex
    dwelling_data: pd.DataFrame = dwelling_type_bedrooms_2021.loc[geo_code, (relevant_housing,)].unstack(level=1)
    dwelling_data = dwelling_data.T
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

    # Drop total number of bedrooms
    dwelling_data = dwelling_data.drop(index=["Total - Number of bedrooms"])
    return dwelling_data