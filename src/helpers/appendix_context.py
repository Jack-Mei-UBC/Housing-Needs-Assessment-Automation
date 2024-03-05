from docxtpl import DocxTemplate

import report_input
from helpers.appendix.table41 import get_table41
from helpers.appendix.table42 import get_table42
from helpers.appendix.table43 import get_table43
from helpers.appendix.table44 import get_table44
from helpers.appendix.table45 import get_table45
from helpers.appendix.table46 import get_table46
from helpers.appendix.table47 import get_table47
from helpers.appendix.table48 import get_table48
from helpers.appendix.table49 import get_table49
from helpers.appendix.table50 import get_table50
from helpers.appendix.table51 import get_table51
from helpers.appendix.table52 import get_table52
from helpers.appendix.table53 import get_table53
from helpers.appendix.table54_56 import get_table54_56
from helpers.appendix.table57_59 import get_table57_59
from helpers.context_helpers import df_to_table_with_columns


def appendix_context(focus: int, doc: DocxTemplate):
    context = {
        # Population tables (2006, 2011, 2016, 2021)
        "table41": df_to_table_with_columns(get_table41(focus)),
        # Headship rate by region (2006, 2021)
        "table42": df_to_table_with_columns(get_table42([report_input.community_cd, report_input.community_csd])),
        # Dwellings by year of construction (cumulative)
        "table43": df_to_table_with_columns(get_table43(focus)),
        # Dwellings by structural type and year of construction
        "table44": df_to_table_with_columns(get_table44(focus)),
        # Dwellings by structural type and number of bedrooms
        "table45": df_to_table_with_columns(get_table45(focus)),
        # Income cost tables 2016
        "table46": df_to_table_with_columns(get_table46(report_input.community_cd)),
        "table47": df_to_table_with_columns(get_table47(report_input.community_csds)),
        # Shelter cost tables 2016
        "table48": df_to_table_with_columns(get_table48(report_input.community_cd)),
        "table49": df_to_table_with_columns(get_table49(report_input.community_csds)),
        # Income cost tables 2021
        "table50": df_to_table_with_columns(get_table50(report_input.community_cd)),
        "table51": df_to_table_with_columns(get_table51(report_input.community_csds)),
        # Shelter cost tables 2021
        "table52": df_to_table_with_columns(get_table52(report_input.community_cd)),
        "table53": df_to_table_with_columns(get_table53(report_input.community_csds)),
        # Total households by hh size
        "table54": df_to_table_with_columns(get_table54_56([report_input.community_cd] + report_input.community_csds, 2006)),
        "table55": df_to_table_with_columns(get_table54_56([report_input.community_cd] + report_input.community_csds, 2016)),
        "table56": df_to_table_with_columns(get_table54_56([report_input.community_cd] + report_input.community_csds, 2021)),
        # Total households by income
        "table57": df_to_table_with_columns(get_table57_59([report_input.community_cd] + report_input.community_csds, 2006)),
        "table58": df_to_table_with_columns(get_table57_59([report_input.community_cd] + report_input.community_csds, 2016)),
        "table59": df_to_table_with_columns(get_table57_59([report_input.community_cd] + report_input.community_csds, 2021)),

    }
    return context
