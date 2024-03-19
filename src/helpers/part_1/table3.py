import pandas as pd
from helpers.data_parsing.table_import import comprehensive_2006, comprehensive_2011, comprehensive_2016, \
    comprehensive_2021

labels = ["Median Age", "Population", "% of population aged 15+", "% of population aged 65+"]


def get_table3(geo_code: int) -> pd.DataFrame:
    df_table3 = pd.DataFrame(
        index=labels,
        columns=[2006, 2011, 2016, 2021]
    )
    df_table3.at[labels[0], 2006] = comprehensive_2006.at[geo_code, ("total by gender", "median age")]
    df_table3.at[labels[0], 2011] = comprehensive_2011.at[geo_code, ("total by gender", "median age")]
    df_table3.at[labels[0], 2016] = comprehensive_2016.at[geo_code, ("total by gender", "median age")]
    df_table3.at[labels[0], 2021] = comprehensive_2021.at[geo_code, ("total by gender", "median age")]

    df_table3.at[labels[1], 2006] = comprehensive_2006.at[geo_code, ("total by gender", 'total by age')]
    df_table3.at[labels[1], 2011] = comprehensive_2011.at[geo_code, ("total by gender", 'population')]
    df_table3.at[labels[1], 2016] = comprehensive_2016.at[geo_code, ("total by gender", 'population')]
    df_table3.at[labels[1], 2021] = comprehensive_2021.at[geo_code, ("total by gender", 'population')]

    flat_2006 = comprehensive_2006.xs('total by gender', axis=1, level=0)
    flat_2011 = comprehensive_2011.xs('total by gender', axis=1, level=0)
    flat_2016 = comprehensive_2016.xs('total by gender', axis=1, level=0)
    flat_2021 = comprehensive_2021.xs('total by gender', axis=1, level=0)

    population_2006 = flat_2006.loc[geo_code, [f'{x} to {x + 4} years' for x in range(0, 96, 5)] + ['100 years+']].sum()
    population_2011 = flat_2011.loc[geo_code, [f'{x} to {x + 4} years' for x in range(0, 81, 5)] + ['85 years+']].sum()
    population_2016 = flat_2016.loc[geo_code, [f'{x} to {x + 4} years' for x in range(0, 81, 5)] + ['85 years+']].sum()
    population_2021 = flat_2021.loc[geo_code, [f'{x} to {x + 4} years' for x in range(0, 81, 5)] + ['85 years+']].sum()

    df_table3.at[labels[2], 2006] = \
        flat_2006.loc[geo_code, [f'{x} to {x + 4} years' for x in range(15, 96, 5)] + ['100 years+']].sum() / population_2006
    df_table3.at[labels[3], 2006] = \
        flat_2006.loc[geo_code, [f'{x} to {x + 4} years' for x in range(65, 96, 5)] + ['100 years+']].sum() / population_2006
    df_table3.at[labels[2], 2011] = \
        flat_2011.loc[geo_code, [f'{x} to {x + 4} years' for x in range(15, 81, 5)] + ['85 years+']].sum() / population_2011
    df_table3.at[labels[3], 2011] = \
        flat_2011.loc[geo_code, [f'{x} to {x + 4} years' for x in range(65, 81, 5)] + ['85 years+']].sum() / population_2011
    # 2016 and 2021 have 85 years+ show up twice, one for ppl in age range, one for PHM maintainers
    df_table3.at[labels[2], 2016] = \
        (flat_2016.loc[geo_code, [f'{x} to {x + 4} years' for x in range(15, 81, 5)]].sum() +
         flat_2016.loc[geo_code, ["85 years+"]].iat[0]) \
         / population_2016
    df_table3.at[labels[3], 2016] = \
        (flat_2016.loc[geo_code, [f'{x} to {x + 4} years' for x in range(65, 81, 5)]].sum() +
         flat_2016.loc[geo_code, ["85 years+"]].iat[0]) \
         / population_2016
    df_table3.at[labels[2], 2021] = \
        (flat_2021.loc[geo_code, [f'{x} to {x + 4} years' for x in range(15, 81, 5)]].sum() +
         flat_2021.loc[geo_code, ["85 years+"]].iat[0]) \
        / population_2021
    df_table3.at[labels[3], 2021] = \
        (flat_2021.loc[geo_code, [f'{x} to {x + 4} years' for x in range(65, 81, 5)]].sum() +
         flat_2021.loc[geo_code, ["85 years+"]].iat[0]) \
        / population_2021

    # Make populations integers
    df_table3.loc[labels[1], :] = df_table3.loc[labels[1], :].astype(int)

    # Make percentages actually percent
    df_table3.loc[(labels[2], labels[3]), :] = (df_table3.loc[(labels[2], labels[3]), :]*100).astype(float).round().astype(int).astype(str) + "%"
    return df_table3


# get_table3(4806)