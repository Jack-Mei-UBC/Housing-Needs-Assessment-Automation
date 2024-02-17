import re

import pandas as pd
import numpy as np

from helpers.data_parsing.column_mapping import col_map, fuzzy_col_mapping


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
    df = df.replace(r'(F|X|x|\.\.)', '0', regex=True).astype(float)
    # Each census, the column names are different, so we need to find a way to standardize them
    # I do this by finding common keywords using a predefined mapping
    keys = list(col_map.keys())
    fuzzy_keys = list(fuzzy_col_mapping.keys())

    # If this is a multi-indexed column dataframe
    if isinstance(df.columns, pd.MultiIndex):
        for index, level in enumerate(df.columns.levels):
            new_label_list = []
            for label in level:
                # First tries fuzzy matching, then exact matching, then gives up and doesn't convert
                try:
                    new_key = next(key for key in fuzzy_keys if re.match(key, label.strip()))
                    new_key = fuzzy_col_mapping[new_key]
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
                new_key = fuzzy_col_mapping[new_key]
            except StopIteration:
                if label.strip() in keys:
                    new_key = col_map[label.strip()]
                else:
                    new_key = label.strip()
            new_label_list.append(new_key)
        df.columns = new_label_list

    return df


comprehensive_2006 = "assets/codes/2006_Prov_CDs_CSDs_Population.csv"
comprehensive_2011 = "assets/codes/2011_Prov_CDs_CSDs_Demographics.csv"
comprehensive_2016 = "assets/codes/2016_Prov_CDs_CSDs.csv"
comprehensive_2021 = "assets/codes/2021_Prov_CDs_CSDs.csv"
PHM_2006 = "assets/codes/2006_Prov_CDs_CSDs_Age of PHM.csv"
HART_2006 = "assets/codes/2006_HART_Consolidated.csv"
dwelling_type_bedrooms_2021 = "assets/codes/2021_Prov_CDs_CSDs_Dwelling type_Bedrooms.csv"
dwelling_type_period_2021 = "assets/codes/2021_Prov_CDs_CSDs_Dwelling type_Period.csv"


comprehensive_2006 = standardize_dataframe(comprehensive_2006)
comprehensive_2011 = standardize_dataframe(comprehensive_2011)
comprehensive_2016 = standardize_dataframe(comprehensive_2016)
comprehensive_2021 = standardize_dataframe(comprehensive_2021)

PHM_2006 = standardize_dataframe(PHM_2006)
HART_2006 = standardize_dataframe(HART_2006)
dwelling_type_bedrooms_2021 = standardize_dataframe(dwelling_type_bedrooms_2021)
dwelling_type_period_2021 = standardize_dataframe(dwelling_type_period_2021)
