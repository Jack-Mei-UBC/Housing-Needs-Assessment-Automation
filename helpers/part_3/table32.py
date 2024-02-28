import pandas as pd

from helpers.context_helpers import get_community_name
from helpers.data_parsing.tables import bedrooms


def get_table32(geo_code: int):
    beds = [1, 2, 3, 4, 5]
    income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']
    geography = get_community_name(geo_code)
    row = bedrooms.loc[geography, :]
    df = pd.DataFrame(columns=income_lv_list, index=beds)
    for bed in beds:
        for i in income_lv_list:
            df.loc[bed, i] = row.loc[f"bedroom need delta {bed} bed {i}"]
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


get_table32(1)
