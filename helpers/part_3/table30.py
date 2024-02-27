import pandas as pd

from helpers.context_helpers import get_community_name
from helpers.data_parsing.tables import partners, bedrooms, projections
from helpers.part_3.table28_29 import get_table28_29


def get_table30(geo_code: int):
    df0 = get_table28_29(geo_code, 28)
    df1 = get_table28_29(geo_code, 29)
    return (df0 + df1)


a = get_table30(1)
print()