from docxtpl import DocxTemplate
from datetime import date

import report_input
from helpers.appendix_context import appendix_context
from helpers.context_helpers import get_community_cd
from helpers.part_1.part_2_community_names import community_names_string, single_community_name
from helpers.part_1_context import part_1_context
from helpers.part_2_context import part_2_context

# Import tables here so when we fork the processes later for multiprocessing, the tables are already loaded
import helpers.data_parsing.table_import  # noqa
from helpers.part_3_context import part_3_context

template_name = "hart_template.docx"
doc = DocxTemplate(template_name)
context = {
    'current_date': str(date.today()),
    'community': single_community_name(report_input.community_cd),
    'community_name_list': community_names_string(report_input.geo_code_list),
    'community_cd': get_community_cd(report_input.community_cd),
}
context.update(part_1_context(doc))
context.update(part_2_context(doc))
context.update(part_3_context(doc))
context.update(appendix_context(doc))
doc.render(context)
doc.save("generated_doc.docx")
