import pandas as pd

from helpers.data_parsing.tables import engine


# Function to extract income from the hart2021 db
def get_income(csd: int):
    query = f'''
    select "Median income of household ($)"
    from geocodes_integrated t1, income t2
    where t1.Geography = t2."Formatted Name"
    and t1.Geo_Code = {csd}
    '''
    df = pd.read_sql(query, engine)
    return df.iloc[0, 0]



