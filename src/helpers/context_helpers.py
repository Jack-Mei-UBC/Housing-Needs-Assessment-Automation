import pandas as pd
import re
from docx.shared import Inches
from docxtpl import DocxTemplate, InlineImage

from helpers.data_parsing.tables import image_locations, engine

num_pattern = r"-?\d+"


def df_to_table(df: pd.DataFrame):
    out = []
    for index in list(df.index):
        temp = df.loc[index].apply(lambda num: f"{int(num):,}" if re.fullmatch(num_pattern, str(num)) else num)
        _dict = temp.to_dict()
        _dict['label'] = index
        out.append(_dict)
    return out


def df_to_table_no_comma(df: pd.DataFrame):
    out = []
    for index in list(df.index):
        _dict = df.loc[index].to_dict()
        _dict['label'] = index
        out.append(_dict)
    return out


def df_to_table_with_columns(df: pd.DataFrame):
    out = {}
    if isinstance(df.columns, pd.MultiIndex):
        for i, level in enumerate(df.columns.levels):
            col_span = 1
            for l in range(i + 1, len(df.columns.levels)):
                col_span *= len(df.columns.levels[l])
            out[f"col{i}_span"] = col_span
            repetitions = 1
            for l in range(0, i):
                repetitions *= len(df.columns.levels[l])
            col = list(level) * repetitions
            out[f"col{i}"] = col
    else:
        out["col0"] = list(df.columns)
    data = []
    for index in list(df.index):
        temp = df.loc[index].apply(lambda num: f"{int(num):,}" if re.fullmatch(num_pattern, str(num)) else num)
        row = {
            "label": index,
            "cols": list(temp)
        }
        data.append(row)
    out["data"] = data
    out["title"] = len(out["col0"]) + 1
    return out


def df_to_table_with_label_seperated(df: pd.DataFrame):
    out = []
    for index in list(df.index):
        temp = df.loc[index].apply(lambda num: f"{int(num):,}" if re.fullmatch(num_pattern, str(num)) else num)
        row = {
            "label": index,
            "cols": list(temp)
        }
        out.append(row)
    return out


def df_to_table_grouped(df: pd.DataFrame):
    out = []
    for index in list(df.index):
        temp = df.loc[index].apply(lambda num: f"{int(num):,}" if re.fullmatch(num_pattern, str(num)) else num)
        in_CHN = temp.iloc[0::2]
        pct_CHN = temp.iloc[1::2]
        zipped = []
        for i in range(len(in_CHN)):
            zipped.append((in_CHN.iloc[i], pct_CHN.iloc[i]))
        row = {
            "label": index,
            "cols": zipped
        }
        out.append(row)
    return out


def merge_years(df0: pd.DataFrame, df1: pd.DataFrame) -> pd.DataFrame:
    df1 = df1.rename(columns={
        "CHN": "CHN1",
        "pctCHN": "pctCHN1",
    })
    df = pd.concat([df0, df1], axis=1)
    return df


def image_to_figure(doc: DocxTemplate, name: str):
    return InlineImage(doc, image_locations + name, width=Inches(6.5), height=Inches(3))


# If it's a CSD, return CSD, if it's a geo_code, return geo_code, if it's a region its doomed, return region
def get_cd_code(geo_code: int) -> int:
    return int(str(geo_code)[0:4])


# Given geocode, return name of community
def get_community_name(geo_code: int) -> str:
    query = f'''
        select "Geography"
        from geocodes_integrated t1
        where t1.Geo_Code = {geo_code}
    '''
    df = pd.read_sql(query, engine)
    return df.iloc[0, 0]


# Return Geography name + geo_code code
def get_community_cd(geo_code: int) -> str:
    geo_code = get_cd_code(geo_code)
    return get_community_name(geo_code) + f" ({geo_code})"
