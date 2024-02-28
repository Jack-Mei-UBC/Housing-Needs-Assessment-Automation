from docxtpl import DocxTemplate

import report_input
from helpers.context_helpers import df_to_table_without_label, df_to_table
from helpers.part_1.part_2_community_names import community_names
from helpers.part_3.table28 import get_table28
from helpers.part_3.table29 import get_table29
from helpers.part_3.table30 import get_table30
from helpers.part_3.table31 import get_table31
from helpers.part_3.table32 import get_table32
from helpers.part_3.table33 import get_table33
from helpers.part_3.table34 import get_table34
from helpers.part_3.table35 import get_table35
from helpers.part_3.table36 import get_table36
from helpers.part_3.table37 import get_table37
from helpers.part_3.table38 import get_table38
from helpers.part_3.table39 import get_table39
from helpers.part_3.table40 import get_table40


def part_3_context(doc: DocxTemplate):
    context = {
        # For the 4 region table names
        "part2codes": community_names(report_input.part_2_geo_codes),
        # By bedroom/income
        "table28": df_to_table(get_table28(report_input.community_geo_code)),
        "table29": df_to_table(get_table29(report_input.community_geo_code)),
        "table30": df_to_table(get_table30(report_input.community_geo_code)),
        "table31": df_to_table(get_table31(report_input.community_geo_code)),
        "table32": df_to_table(get_table32(report_input.community_geo_code)),
        # by hh size
        "table33": df_to_table_without_label(get_table33(report_input.part_2_geo_codes)),
        "table34": df_to_table_without_label(get_table34(report_input.part_2_geo_codes)),
        "table35": df_to_table_without_label(get_table35(report_input.part_2_geo_codes)),
        "table36": df_to_table_without_label(get_table36(report_input.part_2_geo_codes)),
        # by income
        "table37": df_to_table_without_label(get_table37(report_input.part_2_geo_codes)),
        "table38": df_to_table_without_label(get_table38(report_input.part_2_geo_codes)),
        "table39": df_to_table_without_label(get_table39(report_input.part_2_geo_codes)),
        "table40": df_to_table_without_label(get_table40(report_input.part_2_geo_codes)),

    }
    return context
