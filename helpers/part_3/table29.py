import pandas as pd

from helpers.context_helpers import get_community_name
from helpers.data_parsing.tables import projections
from helpers.part_3.table30 import get_table30
from helpers.part_3.table31 import get_table31


def get_table29(geo_code: int):
    df_30 = get_table30(geo_code)
    df_31 = get_table31(geo_code)
    df = df_30/df_31 * 100
    df = df.astype(int).astype(str) + '%'
    return df


get_table29(1)
