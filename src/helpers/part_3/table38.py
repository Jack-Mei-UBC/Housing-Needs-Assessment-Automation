from typing import List

import numpy as np

import report_input
from helpers.part_3.table37 import get_table37
from helpers.part_3.table40 import get_table40

hh_size = [1, 2, 3, 4, 5]


def get_table38(geo_code_list: List[int]):
    df_37 = get_table37(geo_code_list)
    df_40 = get_table40(geo_code_list)
    df = df_37/df_40 * 100
    df_broken = df.isin([np.nan, np.inf, -np.inf])
    df[df_broken] = 0
    df = df.astype(int).astype(str) + '%'
    df[df_broken] = "-"
    return df


get_table38(report_input.community_csds)