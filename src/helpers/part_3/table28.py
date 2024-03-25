import pandas as pd

from helpers.data_parsing.tables import projections
from helpers.part_3.table31 import get_table31
from helpers.part_3.table30 import get_table30


def get_table28(geo_code: int):
    df_30 = get_table30(geo_code)
    df_31 = get_table31(geo_code)
    df = df_30-df_31
    return df


get_table28(1)