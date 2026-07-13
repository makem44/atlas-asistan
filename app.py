import streamlit as st
from google import genai
import os

st.set_page_config(page_title="ATLAS | Asistan", layout="wide")

# API Anahtarını güvenli yükle
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Secrets içerisinde GEMINI_API_KEY tanımlı değil!")
    st.stop()

# Client başlat
client = genai.Client(api_key=api_key)

st.title("🧠 ATLAS | Dijital Sağ Kolum")

# Streaming fonksiyonunu daha esnek yapalım
def stream_ai_response(prompt):
    try:
        # İsteği basitleştirelim
        response = client.models.generate_content_stream(
            model='gemini-1.5-flash',
            contents=prompt
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Hata oluştu: {str(e)}"

gorev = st.sidebar.radio("Görev:", ["İçerik Stratejisi", "Emlak İlanı"])
kategori = st.text_input("Girdi:")

if st.button("Üret"):
    with st.chat_message("assistant"):
        st.write_stream(stream_ai_response(f"{kategori} hakkında içerik üret."))
