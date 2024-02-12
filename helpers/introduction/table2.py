import report_input
from helpers.tables import mapped_geo_code


# Get the relevant CSDs

def get_relevant_csd():
    mask = mapped_geo_code["Geo_Code"].isin(report_input.relevant_csds)
    relevant_geos = mapped_geo_code[mask]
    # Create a new DataFrame with the specified columns
    new_df = relevant_geos[['Geography', 'Geo_Code']]

    # Add a new column that checks if 'Geo_Code' is equal to 'Region_Code'
    new_df = new_df.assign(lvl=(new_df['Geo_Code'] == relevant_geos['Region_Code'].astype(int)))
    new_df.loc[:, 'lvl'] = new_df.loc[:, 'lvl'].astype(str)
    new_df.loc[new_df['lvl'] == "True", 'lvl'] = "CD"
    new_df.loc[new_df['lvl'] == "False", 'lvl'] = "CSD"
    relevant_region_table = []
    for row in new_df.index:
        row_data = {}
        for col in new_df.columns:
            row_data[col] = new_df.at[row, col]
        relevant_region_table.append(row_data)
    return relevant_region_table