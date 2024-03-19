from typing import List

import numpy as np

import report_input
from helpers.part_3.table33 import get_table33
from helpers.part_3.table36 import get_table36

hh_size = [1, 2, 3, 4, 5]


def get_table34(geo_code_list: List[int]):
    df_33 = get_table33(geo_code_list)
    df_36 = get_table36(geo_code_list)
    df = df_33/df_36 * 100
    df_broken = df.isin([np.nan, np.inf, -np.inf])
    df[df_broken] = 0
    df = df.astype(int).astype(str) + '%'
    df[df_broken] = "-"
    return df


# get_table34(report_input.community_csds)