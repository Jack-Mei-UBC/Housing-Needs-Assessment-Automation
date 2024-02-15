import itertools

import pandas as pd
from docxtpl import DocxTemplate
from datetime import date
from sqlalchemy import create_engine

import report_input
from helpers.part_1_context import part_1_context

doc = DocxTemplate("hart_template.docx")
context = {
    'current_date': str(date.today()),
    'community_name': report_input.community_name,
}
context.update(part_1_context())
doc.render(context)
doc.save("generated_doc.docx")
