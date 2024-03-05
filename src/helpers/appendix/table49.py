import pandas as pd

import report_input
from helpers.appendix.table48 import get_table48


def get_table49(geo_list):
    df:pd.DataFrame = None
    for geo_code in geo_list:
        if df is None:
            df = get_table48(geo_code)
        else:
            df = pd.concat([df, get_table48(geo_code)], axis=1)

    return df



get_table49(report_input.community_csds)
