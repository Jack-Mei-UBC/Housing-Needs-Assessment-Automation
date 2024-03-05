import os

from helpers.data_parsing.table_names import csv_dict
from .standardize_dataframe import standardize_dataframe


save_location = "assets/pickle/"
if not os.path.exists(save_location):
    os.mkdir(save_location)
# For each csv in codes, create a table in the database

# csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))


for key in csv_dict.keys():
    df = standardize_dataframe(csv_dict[key])
    # replace the 3 instances of "85 years+" with more descriptive names
    # if key == "comprehensive_2016" or key == "comprehensive_2021":
    #     replacements = ["85 years+", "85 years+ percentage of age groups", "85 years+ PHM maintainers"]
    #     replacement_iter = iter(replacements)
    #     level_replacement = df.columns.levels[1]
    #     level_replacement = [next(replacement_iter) if i == "85 years+" else i for i in level_replacement]
    #     df.columns = df.columns.set_levels(level_replacement, level=1)
    df.to_pickle(save_location + key + ".pkl")
