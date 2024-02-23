from docxtpl import DocxTemplate

import report_input
from helpers.context_helpers import df_to_table
from helpers.part_2.table11 import get_table11
from helpers.part_2.table12_14 import get_table12_14
from helpers.part_2.table13 import get_table13


def part_2_context(doc: DocxTemplate):
    context = {
        "table11": df_to_table(get_table11(report_input.community_geo_code)),
        "table12": df_to_table(get_table12_14(report_input.community_geo_code, 2016)),
        "table13": df_to_table(get_table13(report_input.part_2_geo_codes, 2016)),
        "table14": df_to_table(get_table12_14(report_input.community_geo_code, 2021)),
        "table15": df_to_table(get_table13(report_input.part_2_geo_codes, 2021)),
    }
    return context