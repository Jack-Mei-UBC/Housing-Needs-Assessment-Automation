import itertools

import pandas as pd
from docxtpl import DocxTemplate
from datetime import date
from sqlalchemy import create_engine

import report_input
from helpers.introduction.table2 import get_relevant_csd

doc = DocxTemplate("local/hart_template.docx")
context = {
    'current_date': str(date.today()),
    'community_name': report_input.community_name,
    "relevant_region_table": get_relevant_csd(),
}

doc.render(context)
doc.save("generated_doc.docx")
