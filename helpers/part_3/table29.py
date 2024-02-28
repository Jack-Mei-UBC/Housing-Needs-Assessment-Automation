import pandas as pd
import numpy as np
from helpers.context_helpers import get_community_name
from helpers.data_parsing.tables import projections
from helpers.part_3.table30 import get_table30
from helpers.part_3.table31 import get_table31


def get_table29(geo_code: int):
    df_30 = get_table30(geo_code)
    df_31 = get_table31(geo_code)
    df = ((df_30/df_31)-1) * 100
    df[df < -100] = -100
    df_broken = df.isin([np.nan, np.inf, -np.inf])
    df[df_broken] = 0
    df = df.astype(int).astype(str) + '%'
    df[df_broken] = "-"
    return df


get_table29(1)