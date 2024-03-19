import pandas as pd

from helpers.data_parsing.tables import projections
from helpers.part_3.table31 import get_table31


def get_table28(geo_code: int):
    beds = [1, 2, 3, 4, 5]
    income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']
    row = projections.loc[geo_code, :]
    df = pd.DataFrame(columns=income_lv_list, index=beds)
    for bed in beds:
        for i in income_lv_list:
            df.loc[bed, i] = row.loc[f"2031 Projected bedroom need delta {bed} bed {i}"]
    # Get totals for row and columns


    df = df.rename(
        columns={'20% or under': 'veryLow', '21% to 50%': 'low', '51% to 80%': 'moderate',
                 '81% to 120%': 'median', '121% or more': 'high'})
    df = df.rename(
        index={1: "1", 2: "2", 3: "3", 4: "4", 5: "5+"}
    )
    df = df.astype(int)
    df_31 = get_table31(geo_code)
    df_31 = df_31.drop(index="Total", columns="Total")
    # We can't have predictions go negative so cap it off at 0
    negatives = -df_31 > df
    df[negatives] = -df_31[negatives]

    df['Total'] = df.sum(axis=1)
    df.loc['Total'] = df.sum()
    # Rename columns and rows
    return df


# get_table28(3511)