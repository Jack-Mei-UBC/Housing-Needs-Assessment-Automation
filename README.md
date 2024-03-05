# Housing Needs Assessments Automation

This repo is the structure behind the future in-depth HNAs that HART provides.  

The project is built on [Python docx template](https://github.com/elapouya/python-docx-template)
which uses `python-docx` and `jinja` internally, and the report's variables
will reflect this syntax.  

## How to use
1. Install python 3.12 (pip will be included), you may run into this issue with windows 11? [Solution](https://stackoverflow.com/questions/65348890/python-was-not-found-run-without-arguments-to-install-from-the-microsoft-store)
2. Copy the `/assets/` folder from OneDrive into the `src` directory of this project
3. Open the project root in a terminal, and install the necessary packages using `pip install -r requirements.txt`
4. In the terminal, open `/src/`.  Run the python file using `run_me_once` to run the script once. 
This will create all the necessary files for this program

``` 
cd src
python -m run_once.run_me_once
```

5. Run the python file `main.py` to run the script.  This will create the report in the folder, under `generated_doc.docx`

``` 
cd ..
python main.py
```

### How to change the report
All inputs are decided by the `report_input.py` file.  Change the values there, and then re-run `main.py`.

## Project breakdown
Like mentioned earlier, this is written with python-docx-template as its backbone.  As such, half the work is in the docx
file, the other half in python.  All anchors currently belong in the `hart_template.docx`, and values are provided by
the`context` dictionary in the `main.py` file.

The context dictionary if filled by the functions in `/helpers/`.  These functions create data for each part of the report,
and are organized as they appear in the report.  Each file name corresponds to the tables/figures they are responsible
for providing data for.