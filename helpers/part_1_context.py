import pandas as pd

from helpers.introduction.table2 import get_table2
from helpers.part_1.table3 import get_table3
import report_input

def df_to_table(df:pd.DataFrame):
    out = []
    for index in list(df.index):
        _dict = df.loc[index].to_dict()
        _dict['label'] = index
        out.append(_dict)
    return out
def part_1_context():
    context = {}
    context["table2"] = df_to_table(get_table2())
    context["table3"] = df_to_table(get_table3(report_input.community_csd))
    return context