from typing import List

import pandas as pd

import report_input
from helpers.part_2.table16_19 import get_table16_19


# def place_table13(table: docx.table.Table):

# List should be 4 geocodes
def get_table17(codes: List[int], year: int) -> pd.DataFrame:
    df = get_table16_19(codes[0], year)
    for i in range(1, len(codes)):
        df = pd.concat([df, get_table16_19(codes[i], year)], axis=1)
    # new_columns = []
    # for i in range(8):
    #     new_columns += [f"c{i}"]
    # df.columns = new_columns
    return df

