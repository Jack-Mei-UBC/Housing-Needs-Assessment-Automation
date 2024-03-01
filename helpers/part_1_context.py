from docxtpl import DocxTemplate

import report_input
from helpers.context_helpers import df_to_table, image_to_figure, df_to_table_no_comma
from helpers.introduction.table2 import get_table2
from helpers.part_1.figure2 import get_figure2
from helpers.part_1.figure3 import get_figure3
from helpers.part_1.figure4 import get_figure4
from helpers.part_1.figure5 import get_figure5
from helpers.part_1.figure6 import get_figure6
from helpers.part_1.table10 import get_table10
from helpers.part_1.table3 import get_table3
from helpers.part_1.table4 import get_table4, get_AMHI
from helpers.part_1.table5 import get_table5
from helpers.part_1.table6 import get_table6
from helpers.part_1.table7 import get_table7
from helpers.part_1.table8 import get_table8
from helpers.part_1.table9 import get_table9


def part_1_context(doc: DocxTemplate):

    context = {
        "table2": df_to_table_no_comma(get_table2(report_input.geo_code_list)),
        "table3": df_to_table(get_table3(report_input.community_cd)),
        "table4": df_to_table(get_table4(report_input.community_cd)),
        "table4help": get_AMHI(report_input.community_cd),
        "table5": df_to_table(get_table5(report_input.community_cd)),
        "table6": df_to_table(get_table6(report_input.community_cd)),
        "table7": df_to_table(get_table7(report_input.community_cd)),
        "table8": df_to_table(get_table8(report_input.community_cd)),
        "table9": df_to_table(get_table9(report_input.community_cd)[0]),
        "table9help": get_table9(report_input.community_cd)[1],
        "table10": df_to_table(get_table10(report_input.community_cd)),
        "figure2": image_to_figure(doc, get_figure2(report_input.community_cd)),
        "figure3": image_to_figure(doc, get_figure3(report_input.geo_code_list)),
        "figure4": image_to_figure(doc, get_figure4(report_input.community_cd)),
        "figure5": image_to_figure(doc, get_figure5(report_input.community_cd)),
        "figure6": image_to_figure(doc, get_figure6(report_input.community_cd)),
    }
    return context
