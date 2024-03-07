from typing import Dict

import pandas as pd
from helpers.data_parsing.table_import import consolidated_2016, consolidated_2021, AMHI_2016, AMHI_2021

shelter_cost = [
    "very low shelter cost",
    "low shelter cost",
    "moderate shelter cost",
    "median shelter cost",
    "high shelter cost",
    "total by income"
]


def get_table9(geo_code: int) -> (pd.DataFrame, Dict[str, str]):
    df = pd.DataFrame(
        index=shelter_cost,
        columns=[2016, 2021]
    )

    tables: Dict[int, pd.DataFrame] = {
        2016: consolidated_2016,
        2021: consolidated_2021
    }
    AMHI_tables: Dict[int, pd.DataFrame] = {
        2016: AMHI_2016,
        2021: AMHI_2021
    }

    for year in df.columns:
        # Get any total from level 0 of dataframe
        labels = list(tables[year].columns.levels[0])
        total = next((value for value in labels if 'total' in value.lower()), None)
        # All totals do the same damn thing, please only keep one in the future
        data: pd.Series = tables[year].loc[geo_code, (total, "total by household size", shelter_cost , "total by CHN")]
        data.index = data.index.get_level_values(2)
        df.loc[:, year] = data
    # Add totals
    # df.loc["Total", :] = df.sum()
    # Calculate % changes between 2006 and 2016, then 2016 to 2021 as new columns
    df["change"] = (df[2021] - df[2016]) / df[2016] * 100
    # Make populations integers
    percent_start = 2
    df.iloc[:, :percent_start] = df.iloc[:, :percent_start].astype(int)

    # Make percentages actually percent
    df.iloc[:, percent_start:] = (df.iloc[:, percent_start:]).astype(float).round().astype(int).astype(str) + "%"

    help: Dict[str, str] = {
        "total2016": f"{int(df.iloc[-1, 0]):,}",
        "total2021": f"{int(df.iloc[-1, 1]):,}",
        "change": df.iloc[-1, 2]
    }
    # remove totals now from df
    df = df.drop(index="total by income")

    # Now get the AMHI and merge it into the dataframe
    for year in AMHI_tables.keys():
        # All totals do the same damn thing, please only keep one in the future
        data: pd.Series = AMHI_tables[year].loc[geo_code, :]
        df.loc[:, f"cost{year}"] = data
        help[f"AMHI{year}"] = f"{int(AMHI_tables[year].at[geo_code, 'AMHI']):,}"


    df = df.rename({
        "very low shelter cost": "Very Low",
        "low shelter cost": "Low",
        "moderate shelter cost": "Moderate",
        "median shelter cost": "Median",
        "high shelter cost": "High"
    }, axis=0)
    return df, help


get_table9(3511)