# We seperated the imports into two files because they are slow as hell
# This file is for the consolidated tables
import pandas as pd

from helpers.data_parsing.table_names import save_location

consolidated_2006 = pd.read_pickle(save_location+"consolidated_2006.pkl")
consolidated_2016 = pd.read_pickle(save_location+"consolidated_2016.pkl")
consolidated_2021 = pd.read_pickle(save_location+"consolidated_2021.pkl")
