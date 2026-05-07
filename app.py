import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="Rinrín Renacuajo", layout="wide")

# =========================
# ESTILO VISUAL
# =========================
st.markdown("""
<style>

/* Fondo infantil colorido */
.main {
    background: linear-gradient(135deg, #ff9a9e, #fad0c4, #a18cd1, #fbc2eb);
    background-size: 400% 400%;
    animation: fondo 8s ease infinite;
}

@keyframes fondo {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Título */
h1 {
    text-align: center;
    color: #ffffff;
    font-size: 50px;
    font-weight: 900;
    text-shadow: 0 0 20px #ff4fd8;
}

/* Subtítulos */
h2, h3 {
    color: #ffffff !important;
    text-shadow: 0 0 10px rgba(0,0,0,0.4);
}

/* Texto general */
p, label, span, div {
    color: #ffffff !important;
    font-size: 16px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #6a11cb, #2575fc);
}

/* Botones */
.stButton>button {
    background: linear-gradient(90deg, #ff4fd8, #6a11cb);
    color: white;
    font-weight: bold;
    border-radius: 0px;
    height: 50px;
    border: none;
    font-size: 18px;
}

.stButton>button:hover {
    transform: scale(1.05);
    filter: brightness(1.2);
}

/* Caja de texto */
textarea {
    background-color: rgba(255,255,255,0.15) !important;
    color: white !important;
}

/* Audio */
audio {
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# =========================
# APP
# =========================
st.title("🐸 RINRÍN RENACUAJO")

image = Image.open('rinrin.jpg')
st.image(image, width=350)

with st.sidebar:
    st.subheader("🎧 Escribe o selecciona texto para escucharlo")

# Crear carpeta temporal
try:
    os.mkdir("temp")
except:
    pass

# =========================
# TEXTO
# =========================
st.subheader("📖 Cuento corto")
st.write("""El hijo de rana, Rinrín renacuajo; 
Salió esta mañana muy tieso y muy majo;
Con pantalón corto, corbata a la moda;
Sombrero encintado y chupa de boda.;
-¡Muchacho, no salgas!- le grita mamá;
pero él hace un gesto y orondo se va
... (Rafael Pombo)""")

st.markdown("💬 Copia o escribe el texto para escucharlo")

text = st.text_area("Texto a convertir en audio")

# =========================
# LENGUAJE
# =========================
option_lang = st.selectbox("🌎 Selecciona el lenguaje", ("Español", "English"))

lg = "es" if option_lang == "Español" else "en"

# =========================
# FUNCIÓN TTS
# =========================
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    name = text[0:20] if len(text) > 0 else "audio"
    tts.save(f"temp/{name}.mp3")
    return name

# =========================
# BOTÓN
# =========================
if st.button("🔊 Convertir a audio"):

    if text.strip() != "":

        result = text_to_speech(text, lg)

        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()

        st.markdown("### 🎧 Tu audio")
        st.audio(audio_bytes, format="audio/mp3")

        # Descarga
        bin_str = base64.b64encode(audio_bytes).decode()
        href = f'<a href="data:audio/mp3;base64,{bin_str}" download="audio.mp3">📥 Descargar audio</a>'
        st.markdown(href, unsafe_allow_html=True)

    else:
        st.warning("Escribe un texto primero.")

# =========================
# LIMPIEZA
# =========================
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    now = time.time()
    n_days = n * 86400

    for f in mp3_files:
        if os.stat(f).st_mtime < now - n_days:
            os.remove(f)

remove_files(7)
