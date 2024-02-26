from docxtpl import DocxTemplate
from datetime import date

import report_input
from helpers.context_helpers import get_community_cd
from helpers.part_1_context import part_1_context
from helpers.part_2_context import part_2_context

# Import tables here so when we fork the processes later for multiprocessing, the tables are already loaded
import helpers.data_parsing.table_import  # noqa


template_name = "hart_template.docx"
doc = DocxTemplate(template_name)
context = {
    'current_date': str(date.today()),
    'community_name': report_input.community_name,
    'community_cd': get_community_cd(report_input.community_geo_code),
}
context.update(part_1_context(doc))
context.update(part_2_context(doc))
doc.render(context)
doc.save("generated_doc.docx")
