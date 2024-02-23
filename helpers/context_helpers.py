import pandas as pd
from docx.shared import Inches
from docxtpl import DocxTemplate, InlineImage

from helpers.data_parsing.tables import image_locations, engine


def df_to_table(df: pd.DataFrame):
    out = []
    for index in list(df.index):
        _dict = df.loc[index].to_dict()
        _dict['label'] = index
        out.append(_dict)
    return out


def df_to_table_with_column_label(df: pd.DataFrame):
    out = []
    out.append([]+df.columns.to_list())
    for index in list(df.index):
        _dict = df.loc[index].to_dict()
        _dict['label'] = index
        out.append(_dict)
    return out

def image_to_figure(doc: DocxTemplate, name: str):
    return InlineImage(doc, image_locations + name, width=Inches(6.5), height=Inches(3))


# If it's a CSD, return CSD, if it's a CD, return CD, if it's a region its doomed, return region
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


# Return Geography name + CD code
def get_community_cd(geo_code: int) -> str:
    geo_code = get_cd_code(geo_code)
    return get_community_name(geo_code) + f" ({geo_code})"
