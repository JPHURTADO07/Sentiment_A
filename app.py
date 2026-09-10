from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from googletrans import Translator
import json
from streamlit_lottie import st_lottie

# 1. Creamos una función para cargar los archivos JSON de Lottie
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st.title('Análisis de Sentimiento')

# Manejo de error por si no encuentra la imagen inicial
try:
    image = Image.open('emoticones.jpg')
    st.image(image)
except FileNotFoundError:
    st.warning("No se encontró la imagen 'emoticones.jpg'. Asegúrate de que esté en la misma carpeta.")

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

translator = Translator()

# 2. Cargamos las animaciones (asegúrate de que los nombres coincidan exactamente)
lottie_happy = load_lottiefile("Happy.json")
lottie_sad = load_lottiefile("Sad.json")
lottie_neutral = load_lottiefile("Neutral.json")

with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    st.write("""
    Polaridad: Indica si el sentimiento expresado en el texto es positivo, negativo o neutral. 
    Su valor oscila entre -1 (muy negativo) y 1 (muy positivo), con 0 representando un sentimiento neutral.
    
    Subjetividad: Mide cuánto del contenido es subjetivo (opiniones, emociones, creencias) frente a objetivo
    (hechos). Va de 0 a 1, donde 0 es completamente objetivo y 1 es completamente subjetivo.
    """) 

with st.expander('Analizar texto'):
    text = st.text_input('Escribe por favor: ')
    if text:
        # Traducción y análisis
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)
        
        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)
        
        st.write('Polarity: ', polarity)
        st.write('Subjectivity: ', subjectivity)
        
        # 3. Lógica corregida y renderizado de las animaciones Lottie
        if polarity > 0.0:
            st.success('Es un sentimiento Positivo 😊')
            st_lottie(lottie_happy, width=350)
            st.balloons() # Dejé los globos de Streamlit porque combinan muy bien con lo positivo
            
        elif polarity < 0.0:
            st.error('Es un sentimiento Negativo 😔')
            st_lottie(lottie_sad, width=350)
            
        else:
            st.info('Es un sentimiento Neutral 😐')
            st_lottie(lottie_neutral, width=350)
