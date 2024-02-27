import pandas as pd

from helpers.context_helpers import get_community_name
from helpers.data_parsing.tables import partners, bedrooms, projections


def get_table28_29(geo_code: int, table: int):
    beds = [1, 2, 3, 4, 5]
    income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']
    geography = get_community_name(geo_code)
    if table == 28:
        row = bedrooms.loc[geography, :]
    else:
        row = projections.loc[geo_code, :]
    df = pd.DataFrame(columns=income_lv_list, index=beds)
    for bed in beds:
        for i in income_lv_list:
            if table == 28:
                df.loc[bed, i] = row.loc[f"bedroom need {bed} bed {i}"]
            else:
                df.loc[bed, i] = row.loc[f"2031 Projected bedroom need delta {bed} bed {i}"]
    # Get totals for row and columns
    df['Total'] = df.sum(axis=1)
    df.loc['Total'] = df.sum()
    # Rename columns and rows
    df = df.rename(
        columns={'20% or under': 'veryLow', '21% to 50%': 'low', '51% to 80%': 'moderate',
                 '81% to 120%': 'median', '121% or more': 'high'})
    df = df.rename(
        index={5: "5+"}
    )
    return df


get_table28_29(1, 28)
