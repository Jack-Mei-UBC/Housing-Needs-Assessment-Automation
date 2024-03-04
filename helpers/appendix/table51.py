import pandas as pd

import report_input
from helpers.appendix.table46 import get_table46
from helpers.appendix.table50 import get_table50


def get_table51(geo_list):
    df:pd.DataFrame = None
    for geo_code in geo_list:
        if df is None:
            df = get_table50(geo_code)
        else:
            df = pd.concat([df, get_table50(geo_code)], axis=1)

    return df



get_table51(report_input.community_csds)
