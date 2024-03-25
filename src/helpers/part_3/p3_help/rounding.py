import pandas as pd


def my_round(x: float) -> int:
    if x >= 1000:
        return round(x, -2)
    else:
        return round(x, -1)


def round_df(df: pd.DataFrame) -> pd.DataFrame:
    # If the population prediction is 800+, round to hundreds, else round to tens
    return df.map(my_round)
