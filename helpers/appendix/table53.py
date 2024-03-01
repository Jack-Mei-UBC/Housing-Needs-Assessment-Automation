import pandas as pd

import report_input
from helpers.appendix.table52 import get_table52


def get_table53(geo_list):
    df:pd.DataFrame = None
    for geo_code in geo_list:
        if df is None:
            df = get_table52(geo_code)
        else:
            df = pd.concat([df, get_table52(geo_code)], axis=1)

    return df



get_table53(report_input.geo_code_list)
