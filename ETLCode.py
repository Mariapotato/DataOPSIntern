import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy import Integer, Text, Float

# Шаг 1: Загрузка данных
url = "https://beta.apicrafter.ru/tables/datamos/prognozpogody/export/csv"  
response = requests.get(url)
raw_filename = "weather_forecast_raw.csv"
with open(raw_filename, "wb") as f:
    f.write(response.content)
