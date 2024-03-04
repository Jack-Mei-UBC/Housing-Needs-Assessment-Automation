# How to use
Run the python file `run_me_once.py` to run the script once. This will create all the 
necessary files for this program 
to work properly.  The reason why this was implemented was speed up runtime for subsequent runs.

### `run_once` breakdown
`bedroom_CHN.py` is a legacy file that was used to create the `bedroom_CHN.csv` file. This file is not actually run at 
any point of the program, and is left as reference for any future devs.

`column_mapping.py` is a mapping for the canada census data.  Every damn year uses a slightly different name for a lot 
of data so I made this easier to query for data using "standardized" names.  While this fixes 80% of file issues,
sometimes data is too different to fix (eg. 75+ vs 85+ for primary household maintainer age).  

`convert_database.py` takes existing csvs and converts them into multi-indexed pandas dataframes, then saves them as 
pickle files.  While this is memory intensive, it is much faster to load than the csvs.  This process also uses
`column_mapping.py` to standardize the column names.

`convert_to_code.py` fixes the column names of the csvs.  The are originally saved as the name of the geography and 
geocode, but since we only care about the geocode, this script removes the geography name.  It also fixes two tables
which lack geocodes in their names.

`standardize_dataframe.py` is run by `convert_database.py` to standardize the column names of the dataframes.  