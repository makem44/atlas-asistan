import streamlit as st
from google import genai

# 1. Sayfa Ayarları (EN ÜSTTE)
st.set_page_config(page_title="ATLAS | Asistan", page_icon="🧠", layout="wide")

# 2. Bağlantı Kontrolü (Hata buraya düşerse st.stop() ile uygulama durur)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("API Anahtarı bulunamadı! Secrets ayarlarını kontrol et.")
    st.stop()

# 3. Arayüz (set_page_config sonrası olduğu için artık hata vermez)
st.title("🧠 ATLAS | Dijital Sağ Kolum")
st.sidebar.success("Sistem Bağlantısı Başarılı!")

gorev = st.sidebar.radio("Görev Seç:", ["İçerik Stratejisi", "Emlak İlanı"])

if gorev == "İçerik Stratejisi":
    kategori = st.text_input("Kategori:")
    if st.button("Üret"):
        st.write(f"{kategori} için içerik hazırlanıyor...")