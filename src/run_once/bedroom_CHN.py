import pandas as pd


def bedroom_map(type, hh_size):
    # extract int from hh_size
    hh_size = int(hh_size[0])
    if type == "Without children":
        return 1
    elif type == "With children":
        return hh_size - 1
    elif type == 'One-census-family household without additional persons: one-parent family':
        return hh_size
    elif type == 'One-census-family households with additional persons':
        return hh_size - 1
    elif type == 'One-census-family household with additional persons: one-parent family':
        return hh_size
    elif type == 'Multiple-census-family household':
        return hh_size - 2
    else:
        return hh_size


df = pd.read_csv("assets/2021_Unit_Mix_Consolidated.csv", header=[0, 1, 2, 3], index_col=0, encoding='latin-1')
df = df.replace(r'(F|X|x|\.\.)', '0', regex=True).astype(float)

# Strip all whitespaces from the column multiindex labels
for i in range(len(df.columns.levels)):
    df.columns = df.columns.set_levels(df.columns.levels[i].str.strip(), level=i)

incomes = ['very low income', 'low income', 'moderate income', 'median income', 'high income']
income_map = {
    'Households with household income 121% and over of AMHI': "high income",
    'Households with household income 20% or under of area median household income (AMHI)': "very low income",
    'Households with household income 21% to 50% of AMHI': "low income",
    'Households with household income 51% to 80% of AMHI': "moderate income",
    'Households with household income 81% to 120% of AMHI': "median income",
}
CHN_map = {
    'Households in core housing need status': "CHN",
    'Total - Private Households by core housing need status': "Total",
}
beds = [1, 2, 3, 4, 5]

# We only care about CHN


# Calculate the number of missing bedrooms using the HNA methodology listed on the website
def add_columns(row: pd.Series):
    # Generate the output row that we append into our current SQL table
    CHN = 'CHN'
    total = 'Total'
    CHN_list = [CHN, total]
    output = pd.Series(index=pd.MultiIndex.from_product([beds, CHN_list, incomes], names=['bedrooms', 'chn status', 'income']))
    output.iloc[:] = 0
    # Our current bedroom count x income matrix but flattened

    # Fill HH type x HH size matrix
    for c_i, CHN_status in enumerate(row.index.levels[0]):
        for i, income in enumerate(row.index.levels[2]):
            # Iterate through housing type x hh size matrix at each income level to generate bedroom count x income matrix
            for type in row.index.levels[1]:  # Index is Housing Type
                for hh_size in row.index.levels[3]:  # Columns are HH size
                    bed = bedroom_map(type, hh_size)
                    if bed < 1 or bed > 5:
                        continue
                    output[(bed, CHN_map[CHN_status], income_map[income])] += row[CHN_status, type, income, hh_size]

    return output


output: pd.DataFrame = df.apply(add_columns, axis=1)
output.to_csv("assets/2021_income_bedroom.csv")
