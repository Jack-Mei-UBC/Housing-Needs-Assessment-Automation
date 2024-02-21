from docxtpl import DocxTemplate

import report_input
from helpers.context_helpers import df_to_table
from helpers.part_2.table11 import get_table11


def part_2_context(doc: DocxTemplate):
    context = {
        "table11": df_to_table(get_table11(report_input.community_csd)),
    }
    return context