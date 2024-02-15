import pandas as pd
import plotly.graph_objects as go
import numpy as np

import report_input
from helpers.data_parsing.data_reader import comprehensive_2006, comprehensive_2011, comprehensive_2016, \
    comprehensive_2021


def get_figure2(cd: int) -> str:
    title = f"Population by Age, 2006-2021 = [{report_input.community_name}]"
    df = pd.DataFrame(
        index=["0 to 14 years"] + [f"{x} to {x + 9} years" for x in range(15, 75, 10)] + ["85+ years"],
        columns=[2006, 2011, 2016, 2021]
    )

    flattened_dfs = {
        2006: comprehensive_2006.xs('total by gender', axis=1, level=0),
        2011: comprehensive_2011.xs('total by gender', axis=1, level=0),
        2016: comprehensive_2016.xs('total by gender', axis=1, level=0),
        2021: comprehensive_2021.xs('total by gender', axis=1, level=0),
    }

    for year in range(2006, 2022, 5):
        for i, index in enumerate(df.index):
            if index == "0 to 14 years":
                df.at[index, year] = flattened_dfs[year].loc[cd, [f'{x} to {x + 4} years' for x in range(0, 10, 5)]].sum()
            elif index == "85+ years":
                if year == 2006:
                    df.at[index, year] = \
                        flattened_dfs[year].loc[cd, [f'{x} to {x + 4} years' for x in range(80, 95, 5)] + ['100 years+']].sum()
                else:
                    df.at[index, year] = flattened_dfs[year].at[cd, '85 years+']
            else:
                # Scuffed way, but it works.  i or i+1 happens to be equal to the year's first number
                df.at[index, year] = flattened_dfs[year].loc[cd, [f'{i}5 to {i}9 years', f'{i + 1}0 to {i + 1}4 years']].sum()
    return title


a = get_figure2(report_input.community_csd)
a = 0