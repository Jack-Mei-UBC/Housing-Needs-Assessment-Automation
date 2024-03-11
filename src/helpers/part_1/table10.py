from typing import Dict

import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021, comprehensive_2016, \
    comprehensive_2021

shelter_cost = [
    "owner",
    "owner monthly shelter cost",
    "renter",
    "renter monthly shelter cost"
]


def get_table10(geo_code: int) -> (pd.DataFrame, Dict[str, str]):
    df = pd.DataFrame(
        index=shelter_cost,
        columns=[2016, 2021]
    )

    tables: Dict[int, pd.DataFrame] = {
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    comprehensive_tables: Dict[int, pd.DataFrame] = {
        2016: comprehensive_2016,
        2021: comprehensive_2021
    }

    for year in df.columns:
        # Get any total from level 0 of dataframe
        labels = list(tables[year].columns.levels[0])
        total = next((value for value in labels if 'total' in value.lower()), None)
        # All totals do the same damn thing, please only keep one in the future
        labels_income = list(tables[year].columns.levels[2])
        total_income = next((value for value in labels_income if 'total' in value.lower()), None)
        data: pd.Series = tables[year].loc[geo_code, (total, ("owner", "renter"), total_income, "total by CHN")]
        data.index = data.index.get_level_values(1)
        df.loc[data.index, year] = data

        # repeat for comprehensive tables
        labels = list(comprehensive_tables[year].columns.levels[0])
        total = next((value for value in labels if 'total' in value.lower()), None)
        df_source = comprehensive_tables[year].xs(total, axis=1, level=0)
        data: pd.Series = df_source.loc[geo_code, ["owner monthly shelter cost", "renter monthly shelter cost"]]
        df.loc[data.index, year] = data

    # Add totals
    df.loc["Implied median monthly shelter cost - All Dwellings ($)", :] = \
        (df.loc["owner", :] * df.loc["owner monthly shelter cost", :] +
         df.loc["renter", :] * df.loc["renter monthly shelter cost", :]) / df.loc[["owner", "renter"]].sum(axis=0)
    # Calculate % changes between 2006 and 2016, then 2016 to 2021 as new columns
    df["change"] = (df[2021] - df[2016]) / df[2016] * 100
    # Make populations integers
    percent_start = 2
    df.iloc[:, :percent_start] = df.iloc[:, :percent_start].astype(int)

    # Make percentages actually percent
    df.iloc[:, percent_start:] = (df.iloc[:, percent_start:]).astype(float).round().astype(int).astype(str) + "%"

    # Change these to prices
    indices = [
        "Implied median monthly shelter cost - All Dwellings ($)",
        "owner monthly shelter cost",
        "renter monthly shelter cost"
    ]
    df.loc[indices, [2016, 2021]] = df.loc[indices, [2016, 2021]].map(lambda x: '${:,.0f}'.format(x))

    df = df.rename({
        "owner": "Owner HHs (#)",
        "owner monthly shelter cost": "Median monthly shelter cost - Owned dwellings ($)",
        "renter": "Renter HHs (#)",
        "renter monthly shelter cost": "Median monthly shelter cost - Rented dwellings ($)",
    }, axis=0)
    return df


# get_table10(3511)