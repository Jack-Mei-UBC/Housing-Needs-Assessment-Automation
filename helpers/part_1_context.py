from docxtpl import DocxTemplate

import report_input
from helpers.context_helpers import df_to_table, image_to_figure
from helpers.introduction.table2 import get_table2
from helpers.part_1.figure2 import get_figure2
from helpers.part_1.figure3 import get_figure3
from helpers.part_1.figure4 import get_figure4
from helpers.part_1.figure5 import get_figure5
from helpers.part_1.figure6 import get_figure6
from helpers.part_1.table3 import get_table3
from helpers.part_1.table4 import get_table4
from helpers.part_1.table5 import get_table5
from helpers.part_1.table6 import get_table6
from helpers.part_1.table7 import get_table7
from helpers.part_1.table8 import get_table8
from helpers.part_1.table9 import get_table9


def part_1_context(doc: DocxTemplate):

    context = {
        "table2": df_to_table(get_table2(report_input.relevant_geo_codes)),
        "table3": df_to_table(get_table3(report_input.community_geo_code)),
        "table4": df_to_table(get_table4(report_input.community_geo_code)),
        "table5": df_to_table(get_table5(report_input.community_geo_code)),
        "table6": df_to_table(get_table6(report_input.community_geo_code)),
        "table7": df_to_table(get_table7(report_input.community_geo_code)),
        "table8": df_to_table(get_table8(report_input.community_geo_code)),
        "table9": df_to_table(get_table9(report_input.community_geo_code)),
        "figure2": image_to_figure(doc, get_figure2(report_input.community_geo_code)),
        "figure3": image_to_figure(doc, get_figure3(report_input.relevant_geo_codes[0], report_input.relevant_geo_codes[1])),
        "figure4": image_to_figure(doc, get_figure4(report_input.community_geo_code)),
        "figure5": image_to_figure(doc, get_figure5(report_input.community_geo_code)),
        "figure6": image_to_figure(doc, get_figure6(report_input.community_geo_code)),
    }
    return context
