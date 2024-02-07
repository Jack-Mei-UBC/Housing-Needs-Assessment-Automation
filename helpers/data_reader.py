import pandas as pd
import numpy as np

# Unlike the previous hart project, we're going to use MultiIndex from now on
# Read here if you don't know how it works https://pandas.pydata.org/docs/user_guide/advanced.html
# It's basically a Series, but instead of using 0-n, you can use series[col][col2] to index things
file_name = "../assets/2006_HART_Consolidated.csv"

temp = pd.read_csv(file_name, header=[0, 1, 2], index_col=0, encoding='latin-1')

a = 0
