from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import List

import pandas as pd
#from sklearn.metrics.pairwise import cosine_similarity
#from sklearn.preprocessing import MinMaxScaler

app = FastAPI()

DF_GAMES = pd.read_parquet('Parquets/ETL_Steam_Games.gzip')
DF_REVIEWS = pd.read_parquet('Parquets/Review_Sentiment_Analysis.gzip')
DF_ITEMS = pd.read_parquet('Parquets/ETL_user_items.gzip')
recomendaciones = pd.read_parquet('Parquets/Recomendacion.gzip')

# Función 1
@app.get('/PlayTimeGenre/{genero}')
def play_time_genre(genero: str):
    merged_df = pd.merge(DF_GAMES, DF_ITEMS, on='Item_Id')
    genre_df = merged_df[merged_df['Genres'] == genero]
    grouped_df = genre_df.groupby('Release_Year')['Playtime_Forever'].sum().reset_index()
    max_year = grouped_df.loc[grouped_df['Playtime_Forever'].idxmax(), 'Release_Year']
    result = {"Año de lanzamiento con más horas jugadas para Género " + genero: int(max_year)}
    return result


