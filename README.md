# Housing Needs Assessments Automation

This repo is the structure behind the future in-depth HNAs that HART provides.  

The project is built on [Python docx template](https://github.com/elapouya/python-docx-template)
which uses `python-docx` and `jinja` internally, and the report's variables
will reflect this syntax.  

## How to use
1. Install python 3.11 (pip will be included)
2. Copy the `/assets/` folder from OneDrive into the root of this project
3. Open the directory in a terminal, and run `pip install -r requirements.txt`
4. Run the python file `run_me_once.py` to run the script once. This will create all the necessary files for this program
5. Run the python file `main.py` to run the script.  This will create the report in the folder, under `generated_doc.docx`

### Project breakdown
Like mentioned earlier, this is written with python-docx-template as its backbone.  As such, half the work is in the docx
file, the other half in python.  All anchors currently belong in the `hart_template.docx`, and values are provided by
the`context` dictionary in the `main.py` file.

The context dictionary if filled by the functions in `/helpers/`.  These functions create data for each part of the report,
and are organized as they appear in the report.  Each file name corresponds to the tables/figures they are responsible
for providing data for.