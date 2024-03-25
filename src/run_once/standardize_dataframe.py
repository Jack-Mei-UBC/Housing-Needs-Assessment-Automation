import re

import pandas as pd

from run_once.column_mapping import col_map, fuzzy_regex_col_mapping


# Unlike the previous hart project, we're going to use MultiIndex from now on
# Read here if you don't know how it works https://pandas.pydata.org/docs/user_guide/advanced.html
# It's basically a Series, but instead of using 0-n, you can use series[col][col2] to index things
def standardize_dataframe(file_name):
    # Check the length of the header
    chunk = pd.read_csv(file_name, header=None, chunksize=10, encoding='latin-1')
    chunk = next(chunk)
    header_length = 1
    while header_length < 10:  # If the header is longer than 10 we have different issues now
        if re.match(r'^\d*\.?\d+$', str(chunk.iloc[header_length, 1])) is not None:
            break
        header_length += 1

    df = pd.read_csv(file_name, header=[i for i in range(header_length)], index_col=0, encoding='latin-1')

    # All the data is stored as strings, so we need to convert it to floats
    # Exceptions are the AMHI ones, which are actually strings
    if "AMHI" not in file_name:
        df = df.replace(r'(F|X|x|\.\.)', '0', regex=True).astype(float)
    # Each census, the column names are different, so we need to find a way to standardize them
    # I do this by finding common keywords using a predefined mapping
    keys = list(col_map.keys())
    fuzzy_keys = list(fuzzy_regex_col_mapping.keys())

    # If this is a multi-indexed column dataframe
    if isinstance(df.columns, pd.MultiIndex):
        for index, level in enumerate(df.columns.levels):
            new_label_list = []
            for label in level:
                # First tries fuzzy matching, then exact matching, then gives up and doesn't convert
                try:
                    new_key = next(key for key in fuzzy_keys if re.match(key, label.strip()))
                    new_key = fuzzy_regex_col_mapping[new_key]
                except StopIteration:
                    if label.strip() in keys:
                        new_key = col_map[label.strip()]
                    else:
                        new_key = label.strip()
                new_label_list.append(new_key)
            df.columns = df.columns.set_levels(new_label_list, level=index, verify_integrity=False)

    # Single Index
    else:
        new_label_list = []
        for label in df.columns:
            # First tries fuzzy matching, then exact matching, then gives up and doesn't convert
            try:
                new_key = next(key for key in fuzzy_keys if re.match(key, label.strip()))
                new_key = fuzzy_regex_col_mapping[new_key]
            except StopIteration:
                if label.strip() in keys:
                    new_key = col_map[label.strip()]
                else:
                    new_key = label.strip()
            new_label_list.append(new_key)
        df.columns = new_label_list

    return df
