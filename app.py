import streamlit as st
from google import genai
import os

# 1. EN ÜSTTE OLMASI ZORUNLU
st.set_page_config(page_title="ATLAS | Asistan", page_icon="🧠", layout="wide")

# 2. BAĞLANTI KURULUŞU
@st.cache_resource
def get_client():
    api_key = st.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)

try:
    client = get_client()
    st.sidebar.success("Sistem Bağlantısı Başarılı!")
except Exception as e:
    st.sidebar.error("API Anahtarı bulunamadı! Secrets ayarlarını kontrol et.")
    st.stop()

# 3. UYGULAMA GÖVDESİ
st.title("🧠 ATLAS | Dijital Sağ Kolum")

def stream_ai_response(prompt):
    response = client.models.generate_content_stream(
        model='gemini-1.5-flash',
        contents=prompt
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text

gorev = st.sidebar.radio("Görev Seç:", ["İçerik Stratejisi", "Emlak İlanı"])

if gorev == "İçerik Stratejisi":
    kategori = st.text_input("Kategori:")
    if st.button("Üret"):
        with st.chat_message("assistant"):
            st.write_stream(stream_ai_response(f"{kategori} için strateji yaz."))
