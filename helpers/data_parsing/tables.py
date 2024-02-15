import pandas as pd
from sqlalchemy import create_engine

image_locations = "assets/images"
engine = create_engine(f'sqlite:///assets/hart2021.db')
mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())

