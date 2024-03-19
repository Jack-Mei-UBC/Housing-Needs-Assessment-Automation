import docx
import docx.text.paragraph, docx.table

keys = [
    "Table 28:",
    "Table 29:",
    "Table 30:",
    "Table 31:",
    "Table 32:",
]


def run(output_name: str):
    # Locate anchor
    doc = docx.Document(output_name)
    table = None
    for paragraph in doc.iter_inner_content():
        if isinstance(paragraph, docx.text.paragraph.Paragraph):
            # print(paragraph.text)
            if any([key in paragraph.text for key in keys]):
                bold_last_row(table)
        if isinstance(paragraph, docx.table.Table):
            table = paragraph
    # save doc
    doc.save(output_name)


def bold_last_row(table):
    row = table.rows[-1]
    for cell in row.cells:
        for paragraph in cell.paragraphs:
            run = paragraph.runs[0]
            run.bold = True


# run("generated_doc.docx")