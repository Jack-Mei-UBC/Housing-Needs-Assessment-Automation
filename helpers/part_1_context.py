import pandas as pd
from docxtpl import InlineImage, DocxTemplate
from docx.shared import Inches

from helpers.data_parsing.tables import image_locations
from helpers.introduction.table2 import get_table2
from helpers.part_1.figure2 import get_figure2
from helpers.part_1.figure3 import get_figure3
from helpers.part_1.figure4 import get_figure4
from helpers.part_1.figure5 import get_figure5
from helpers.part_1.figure6 import get_figure6
from helpers.part_1.table3 import get_table3
import report_input


def df_to_table(df: pd.DataFrame):
    out = []
    for index in list(df.index):
        _dict = df.loc[index].to_dict()
        _dict['label'] = index
        out.append(_dict)
    return out


def image_to_figure(doc: DocxTemplate, name: str):
    return InlineImage(doc, image_locations+name, width=Inches(6.5), height=Inches(3))


def part_1_context(doc: DocxTemplate):
    context = {
        "table2": df_to_table(get_table2(report_input.relevant_csds)),
        "table3": df_to_table(get_table3(report_input.community_csd)),
        "figure2": image_to_figure(doc, get_figure2(report_input.community_csd)),
        "figure3": image_to_figure(doc, get_figure3(report_input.relevant_csds[0], report_input.relevant_csds[1])),
        "figure4": image_to_figure(doc, get_figure4(report_input.community_csd)),
        "figure5": image_to_figure(doc, get_figure5(report_input.community_csd)),
        "figure6": image_to_figure(doc, get_figure6(report_input.community_csd)),
    }
    return context
