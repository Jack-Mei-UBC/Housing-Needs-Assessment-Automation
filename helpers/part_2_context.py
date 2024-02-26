from docxtpl import DocxTemplate

import report_input
from helpers.context_helpers import df_to_table
from helpers.part_1.part_2_community_names import community_names
from helpers.part_2.table11 import get_table11
from helpers.part_2.table12_15 import get_table12_15
from helpers.part_2.table13 import get_table13
from helpers.part_2.table16_19 import get_table16_19
from helpers.part_2.table17 import get_table17


def part_2_context(doc: DocxTemplate):
    context = {
        "part2codes": community_names(report_input.part_2_geo_codes),
        "table11": df_to_table(get_table11(report_input.community_geo_code)),
        "table12": df_to_table(get_table12_15(report_input.community_geo_code, 2016)),
        "table13": df_to_table(get_table13(report_input.part_2_geo_codes, 2016)),
        "table14": df_to_table(get_table12_15(report_input.community_geo_code, 2021)),
        "table15": df_to_table(get_table13(report_input.part_2_geo_codes, 2021)),
        "table16": df_to_table(get_table16_19(report_input.community_geo_code, 2016)),
        "table17": df_to_table(get_table17(report_input.part_2_geo_codes, 2016)),
        "table18": df_to_table(get_table16_19(report_input.community_geo_code, 2021)),
        "table19": df_to_table(get_table17(report_input.part_2_geo_codes, 2021)),
    }
    return context