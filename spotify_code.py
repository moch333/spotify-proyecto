#!/usr/bin/env python
# coding: utf-8

#Importamos librerias, imagenes, y la base de datos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import random
from skimage import io
from datetime import datetime

spotify_df = pd.read_csv('./Datos/spotify_songs.csv')

spotify_df = spotify_df.rename(columns = {
'track_id': 'ID', 
'track_name': 'Nombre',
'track_artist': 'Artista',
'track_popularity': 'Popularidad',
'track_album_id': 'album_id',
'track_album_name': 'Nombre del Album',
'track_album_release_date': 'Lanzamiento',
'playlist_name': 'Playlist',
'playlist_genre': 'Genero',
'playlist_subgenre': 'Subgenero',
'danceabillity': 'ritmo',
'energy': 'energia',
'loudness': 'volumen',
'speechiness' : 'voz',
'acousticness' : 'acustica',
'instrumentalness' : 'instrumental',
'liveness' : 'vivo',
'valence' : 'tono',
'tempo' : 'ritmo',
"duration_ms":"Duracion"
    })
spotify_df = spotify_df.dropna()
spotify_df= spotify_df[["Nombre","Artista","Popularidad","Nombre del Album","Lanzamiento","Playlist","Genero","Subgenero","Duracion"]]
spotify_df['Lanzamiento'] = pd.to_datetime(spotify_df['Lanzamiento'], format="mixed")
spotify_df = spotify_df.sort_values(by='Lanzamiento')

# Crear nuevas columnas para el año y el mes
spotify_df['Año'] = spotify_df['Lanzamiento'].dt.year
spotify_df['Mes'] = spotify_df['Lanzamiento'].dt.month

pop_df = spotify_df[spotify_df['Genero'] == 'pop']
rap_df = spotify_df[spotify_df['Genero'] == 'rap']
rock_df = spotify_df[spotify_df['Genero'] == 'rock']
latin_df = spotify_df[spotify_df['Genero'] == 'latin']
rb_df = spotify_df[spotify_df['Genero'] == 'r&b']
edm_df = spotify_df[spotify_df['Genero'] == 'edm']

#Importamos imágenes
sidebar = io.imread(r"./Imagenes/Bar.png")

#Portada
st.title("Análisis de datos de Spotify")
st.subheader(":green[En este proyecto, se pueden observar tres herramientas:]")
st.markdown(":green[**1.** Gráfico que muestra los subgéneros más escuchados por género músical]")
st.markdown(":green[**2.** Gráfico que muestra cuantas canciones fueron lanzadas según el mes]")
st.markdown(":green[**3.** Canción aleatoria con toda su información]")
st.markdown(":green[Esta información se generó gracias al siguiente DataFrame:]")

#DataFrame
st.dataframe(spotify_df)
st.divider()

#Dashboard
st.sidebar.image(sidebar, width=220)
# st.sidebar.markdown("#Configuración")
st.sidebar.divider()

#Definir columnas para gráficas
column_izq, column_der = st.columns(2)

#Gráfico por Género
vars_genero = ["pop", "rap", "rock", "latin", "r&b", "edm"]
default_gen = vars_genero.index("pop")
gen_select = st.sidebar.selectbox("Género para la gráfica", options=vars_genero)
st.sidebar.divider()

column_izq.subheader("Género")
fig1, ax1 = plt.subplots()

if gen_select == "pop":
    grafgen_df = pop_df
elif gen_select == "rap":
    grafgen_df = rap_df
elif gen_select == "rock":
    grafgen_df = rock_df
elif gen_select == "latin":
    grafgen_df = latin_df
elif gen_select == "r&b":
    grafgen_df = rb_df
elif gen_select == "edm":
    grafgen_df = edm_df
else:
    grafgen_df = spotify_df

# Crear el gráfico de barras para los subgéneros
subgen_counts = grafgen_df["Subgenero"].value_counts()
ax1.bar(subgen_counts.index, subgen_counts.values)
ax1.set_title("Género y sus subgéneros más escuchados")
ax1.set_xlabel("Subgénero")
ax1.set_ylabel("Número de canciones")

# Mostrar el gráfico en Streamlit
column_izq.pyplot(fig1)

#Gráfico por Años
vars_año = spotify_df["Año"].unique()
año_select = st.sidebar.selectbox("Año para la gráfica", options=vars_año)
añofilt_df = spotify_df[spotify_df["Año"] == año_select]

column_der.subheader("Lanzamiento")
fig2, ax2 = plt.subplots()

# Contar las canciones por mes en el año seleccionado
mes_counts = añofilt_df.groupby("Mes").size().reset_index(name="Conteo")

# Mapear los meses numéricos a sus nombres en string
mes_names = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", 
    "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Reemplazar los números de mes por los nombres
mes_counts["Mes"] = mes_counts["Mes"].apply(lambda x: mes_names[x-1])

# Crear el gráfico de barras para los meses
ax2.bar(mes_counts["Mes"], mes_counts["Conteo"])
ax2.set_title(f"Canciones lanzadas por mes en el año: {año_select}")
ax2.set_xlabel("Mes")
ax2.set_ylabel("Número de canciones")
plt.xticks(rotation=45, ha="right")

# Mostrar el gráfico en Streamlit
column_der.pyplot(fig2)

st.sidebar.divider()
#Información de Canción
def display_rndm_song(df):
    random_index = random.randint(0, len(df) - 1)
    random_song = spotify_df.iloc[random_index]
    st.write(f"**Nombre:** {random_song['Nombre']}")
    st.write(f"**Artista:** {random_song['Artista']}")
    st.write(f"**Popularidad:** {random_song['Popularidad']}")
    st.write(f"**Nombre del Album:** {random_song['Nombre del Album']}")
    st.write(f"**Lanzamiento:** {random_song['Lanzamiento'].date()}")
    st.write(f"**Playlist:** {random_song['Playlist']}")
    st.write(f"**Subgenero:** {random_song['Subgenero']}")
    st.write(f"**Duracion:** {random_song['Duracion']} seconds")

if st.sidebar.button ("Canción del día"):
    display_rndm_song(spotify_df)

# streamlit run c:/Users/luill/OneDrive/Documentos/Cranopolis/Spotify_code.py
