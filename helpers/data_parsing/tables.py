import pandas as pd
from sqlalchemy import create_engine
import os

image_locations = "assets/images/"
table_locations = "assets/tables/"
if not os.path.exists(image_locations):
    os.mkdir(image_locations)
if not os.path.exists(table_locations):
    os.mkdir(table_locations)
colors = {
    2006: "rgba(196,214,237,255)",
    2011: "rgba(196,214,237,255)",
    2016: "rgba(105,144,195,255)",
    2021: "rgba(47,78,120,255)",
}


engine = create_engine(f'sqlite:///assets/hart2021.db')
mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())

