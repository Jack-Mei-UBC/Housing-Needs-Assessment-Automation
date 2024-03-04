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
dwelling_colors = {
    "Attached, semi-detached, row housing": "rgba(64,64,64,255)",  # Dark Grey
    "Single-detached house": "rgba(125,125,125,255)",  # Grey
    "Apartment in building with 5+ storeys": "rgba(0,114,154,255)",  # Dark Blue
    "Apartment in building with <5 storeys, duplexes": "rgba(77,198,248,255)",  # Light Blue
    "Movable dwelling": "rgba(81,188,91,255)",  # Green
}
bedroom_colors = {
    "1 bedroom": "rgba(77,198,248,255)",  # Light Blue
    "2 bedrooms": "rgba(101,152,209,255)",  # Medium Blue
    "3 bedrooms": "rgba(0,114,154,255)",  # Dark Blue
    "4 or more bedrooms": "rgba(26,55,88,255)",  # Dark Blue
    "No bedrooms": "rgba(81,188,91,255)",  # Green
}

engine = create_engine(f'sqlite:///assets/hart2021.db')
mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())
partners = pd.read_sql_table('partners', engine.connect())
bedrooms = pd.read_sql_table('bedrooms', engine.connect())
bedrooms = bedrooms.set_index("Geography")  # God I hate how lgeo used names instead of geocodes to index
projections = pd.read_sql_table('csd_hh_projections', engine.connect())
# Drop nan rows
projections = projections.dropna()
projections = projections.astype({"Geo_Code": int})
projections = projections.set_index("Geo_Code")
