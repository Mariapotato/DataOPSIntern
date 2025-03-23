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

# Шаг 2: Трансформация данных
df = pd.read_csv(raw_filename)

# Нормализация названий колонок
df.columns = (
    df.columns.str.strip()          # Удаление пробелов по краям
    .str.lower()                    # Приведение к нижнему регистру
    .str.replace(" ", "_")          # Замена пробелов на подчеркивания
)

# Проверка наличия необходимых колонок
required_columns = ["maximumtemperature", "minimumtemperature"]
for col in required_columns:
    if col not in df.columns:
        available = ", ".join(df.columns)
        raise KeyError(f"Колонка {col} не найдена. Доступные колонки: {available}")

# Преобразование температур в числовой формат
df["maximumtemperature"] = pd.to_numeric(df["maximumtemperature"], errors="coerce")
df["minimumtemperature"] = pd.to_numeric(df["minimumtemperature"], errors="coerce")

# Фильтрация данных
filtered_df = df[
    (df["maximumtemperature"] < 20) &
    (df["maximumtemperature"].notna())
]


# Шаг 3: Сохранение результатов
clean_filename = "filtered_forecasts.csv"
filtered_df.to_csv(clean_filename, index=False)

