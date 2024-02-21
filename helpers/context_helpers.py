import pandas as pd
from docx.shared import Inches
from docxtpl import DocxTemplate, InlineImage

from helpers.data_parsing.tables import image_locations


def df_to_table(df: pd.DataFrame):
    out = []
    for index in list(df.index):
        _dict = df.loc[index].to_dict()
        _dict['label'] = index
        out.append(_dict)
    return out


def image_to_figure(doc: DocxTemplate, name: str):
    return InlineImage(doc, image_locations+name, width=Inches(6.5), height=Inches(3))
