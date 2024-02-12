import pandas as pd
import numpy as np

from helpers.data_parsing.column_mapping import col_map

# Unlike the previous hart project, we're going to use MultiIndex from now on
# Read here if you don't know how it works https://pandas.pydata.org/docs/user_guide/advanced.html
# It's basically a Series, but instead of using 0-n, you can use series[col][col2] to index things
file_name = "assets/2006_HART_Consolidated.csv"

# Check the length of the header
chunk = pd.read_csv(file_name,header=None, chunksize=10, encoding='latin-1')
chunk = next(chunk)
header_length = 1
while header_length < 10:  # If the header is longer than 10 we have different issues now
    if str(chunk.iloc[header_length, 1]).isnumeric():
        break
    header_length += 1


temp = pd.read_csv(file_name, header=[i for i in range(header_length)], index_col=0, encoding='latin-1')

# Each census, the column names are different, so we need to find a way to standardize them
# I do this by finding common keywords using a predefined mapping
keys = list(col_map.keys())
for index, level in enumerate(temp.columns.levels):
    new_label_list = []
    for label in level:
        # This might throw an error, if it does, that means we need to add a new key to the mapping
        new_key = next(key for key in keys if key in label)
        new_label_list.append(col_map[new_key])
    temp.columns = temp.columns.set_levels(new_label_list, level=index)


a = 0
