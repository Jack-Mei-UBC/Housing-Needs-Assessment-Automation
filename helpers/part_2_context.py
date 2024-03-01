from docxtpl import DocxTemplate

import report_input
from helpers.context_helpers import df_to_table, df_to_table_with_label_seperated, df_to_table_grouped
from helpers.part_1.part_2_community_names import community_names
from helpers.part_2.table11 import get_table11
from helpers.part_2.table12_15 import get_table12_15
from helpers.part_2.table13 import get_table13
from helpers.part_2.table16_19 import get_table16_19
from helpers.part_2.table17 import get_table17
from helpers.part_2.table20_23 import get_table20_23
from helpers.part_2.table21 import get_table21
from helpers.part_2.table24_27 import get_table24_27
from helpers.part_2.table25 import get_table25


def part_2_context(doc: DocxTemplate):
    context = {
        # For the 4 region table names
        "part2codes": community_names(report_input.geo_code_list),
        #
        "table11": df_to_table(get_table11(report_input.community_cd)),
        # CHN by income
        "table12": df_to_table(get_table12_15(report_input.community_cd, 2016)),
        "table13": df_to_table_grouped(get_table13(report_input.geo_code_list, 2016)),
        "table14": df_to_table(get_table12_15(report_input.community_cd, 2021)),
        "table15": df_to_table_grouped(get_table13(report_input.geo_code_list, 2021)),
        # CHN by HH size
        "table16": df_to_table(get_table16_19(report_input.community_cd, 2016)),
        "table17": df_to_table_grouped(get_table17(report_input.geo_code_list, 2016)),
        "table18": df_to_table(get_table16_19(report_input.community_cd, 2021)),
        "table19": df_to_table_grouped(get_table17(report_input.geo_code_list, 2021)),
        # CHN by tenure
        "table20": df_to_table(get_table20_23(report_input.community_cd, 2016)),
        "table21": df_to_table_grouped(get_table21(report_input.geo_code_list, 2016)),
        "table22": df_to_table(get_table20_23(report_input.community_cd, 2021)),
        "table23": df_to_table_grouped(get_table21(report_input.geo_code_list, 2021)),
        # CHN by Priority Population
        "table24": df_to_table(get_table24_27(report_input.community_cd, 2016)),
        "table25": df_to_table_grouped(get_table25(report_input.geo_code_list, 2016)),
        "table26": df_to_table(get_table24_27(report_input.community_cd, 2021)),
        "table27": df_to_table_grouped(get_table25(report_input.geo_code_list, 2021)),

    }
    return context
