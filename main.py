from docxtpl import DocxTemplate
from datetime import date

import report_input
from helpers.part_1_context import part_1_context

# Import tables here so when we fork the processes later for multiprocessing, the tables are already loaded
import helpers.data_parsing.table_import  # noqa
import run_once.table_import_consolidated  # noqa

doc = DocxTemplate("hart_template.docx")
context = {
    'current_date': str(date.today()),
    'community_name': report_input.community_name,
}
context.update(part_1_context(doc))
doc.render(context)
doc.save("generated_doc.docx")
