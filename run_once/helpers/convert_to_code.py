import re
import os

import pandas as pd

# Grabs all the csvs in the assets directory, changing them only to be codes
all_files = os.listdir("assets")
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))

save_location = "assets/codes/"
if not os.path.exists(save_location):
    os.mkdir(save_location)
processed_files = os.listdir(save_location)
processed_csv_files = list(filter(lambda f: f.endswith('.csv'), processed_files))


def find_code(name):
    pattern = r"\(\d+\)"
    try:
        new_key = next(key for key in fuzzy_keys if re.match(key, name.strip()))
        name = fuzzy_quirky_regions[new_key[2:-2]]
    except StopIteration:
        if name in quirky_regions.keys():
            name = quirky_regions[name]
    code = re.findall(pattern, name)[0]
    code = code[1:-1]
    return code


copy_existing_index = [
    '2021_Prov_CDs_CSDs_Dwelling type_Bedrooms.csv',
    '2021_Prov_CDs_CSDs_Dwelling type_Period.csv',
]

fuzzy_quirky_regions = {
    "Canada": 'Canada (1) 20000 (  4.3%)',
    "Ontario 20010": "Ontario (35) 20010 (  5.0%)",
    'British Columbia 21010 ': 'British Columbia (59) 21010 (  7.5%)',
    'Alberta 21010 (  5.8%)': 'Alberta (48) 21010 (  5.8%)',
    'Manitoba 00010 (  5.0%)': 'Manitoba (46) 00010 (  5.0%)',
    'Saskatchewan 20010 (  5.7%)': 'Saskatchewan (47) 20010 (  5.7%)',
    'Quebec 21010 (  5.6%)': 'Quebec (24) 21010 (  5.6%)',
    'Newfoundland and Labrador 00000 (  4.2%)': 'Newfoundland and Labrador (10) 00000 (  4.2%)',
    'Prince Edward Island 00000': 'Prince Edward Island (11) 00000 (  4.0%)',
    'New Brunswick 00000': 'New Brunswick (13) 00000 (  4.1%)',
    'Nova Scotia 01000': 'Nova Scotia (12) 01000 (  4.7%)',
    'Yukon 00010': 'Yukon (60) 00010 (  7.2%)',
    'Northwest Territories 00000': 'Northwest Territories (61) 00000 (  4.7%)',
    'Nunavut 00010': 'Nunavut 00010 (62) (  5.9%)',
}
fuzzy_keys = fuzzy_quirky_regions.keys()
fuzzy_keys = [f".*{key}.*" for key in fuzzy_keys]

quirky_regions = {
    "Ontario 20010 (  5.0%)": "Ontario (35) 20010 (  5.0%)",
    'British Columbia 21010 (  7.5%)': 'British Columbia (59) 21010 (  7.5%)',
    'Alberta 21010 (  5.8%)': 'Alberta (48) 21010 (  5.8%)',
    'Manitoba 00010 (  5.0%)': 'Manitoba (46) 00010 (  5.0%)',
    'Saskatchewan 20010 (  5.7%)': 'Saskatchewan (47) 20010 (  5.7%)',
    'Quebec 21010 (  5.6%)': 'Quebec (24) 21010 (  5.6%)',
    'Newfoundland and Labrador 00000 (  4.2%)': 'Newfoundland and Labrador (10) 00000 (  4.2%)',
    'Newfoundland and Labrador': 'Newfoundland and Labrador (10) 00000 (  4.2%)',
    'Prince Edward Island 00000 (  4.0%)': 'Prince Edward Island (11) 00000 (  4.0%)',
    'New Brunswick 00000 (  4.1%)': 'New Brunswick (13) 00000 (  4.1%)',
    'Nova Scotia 01000 (  4.7%)': 'Nova Scotia (12) 01000 (  4.7%)',
    'Yukon 00010 (  7.2%)': 'Yukon (60) 00010 (  7.2%)',
    'Northwest Territories 00000 (  4.7%)': 'Northwest Territories (61) 00000 (  4.7%)',
    'Nunavut 00010 (  5.9%)': 'Nunavut 00010 (62) (  5.9%)',
    'Canada 20000 (  4.3%)': 'Canada (1) 20000 (  4.3%)',
    'Canada': 'Canada (1) 20000 (  4.3%)',
}
# Extract geocode from the name
for csv_file in csv_files:
    if csv_file in processed_csv_files or csv_file in copy_existing_index:
        continue
    chunk = pd.read_csv("assets/" + csv_file, header=None, chunksize=10, encoding='latin-1')
    chunk = next(chunk)
    header_length = 1
    while header_length < 10:  # If the header is longer than 10 we have different issues now
        if re.match(r'^\d*\.?\d+$', str(chunk.iloc[header_length, 1])) is not None:
            break
        header_length += 1

    temp = pd.read_csv("assets/" + csv_file, header=[i for i in range(header_length)], index_col=0, encoding='latin-1')

    new_index = temp.index.to_series().apply(find_code)
    temp = temp.set_index(new_index)
    temp.to_csv("assets/codes/" + csv_file)

working_CSDs = pd.read_csv("assets/codes/" + "2021_Prov_CDs_CSDs.csv", header=[0, 1], index_col=0, encoding='latin-1')
original_CSDs = pd.read_csv("assets/" + "2021_Prov_CDs_CSDs.csv", header=[0, 1], index_col=0, encoding='latin-1')
# Copy the indexes from another csv if they match
for csv_file in csv_files:
    if csv_file in processed_csv_files or csv_file not in copy_existing_index:
        continue
    chunk = pd.read_csv("assets/" + csv_file, header=None, chunksize=10, encoding='latin-1')
    chunk = next(chunk)
    header_length = 1
    while header_length < 10:  # If the header is longer than 10 we have different issues now
        if re.match(r'^\d*\.?\d+$', str(chunk.iloc[header_length, 1])) is not None:
            break
        header_length += 1

    temp = pd.read_csv("assets/" + csv_file, header=[i for i in range(header_length)], index_col=0, encoding='latin-1')

    for i, label in enumerate(temp.index):
        if label not in original_CSDs.index[i]:
            LookupError(f"{temp.index} not found in index, closest is {original_CSDs.index[i]}")

    temp.index = working_CSDs.index
    temp.to_csv("assets/codes/" + csv_file)
