import streamlit as st
from google import genai

# Sayfa Ayarları
st.set_page_config(page_title="ATLAS | Asistan", page_icon="🧠", layout="wide")

# Güvenli API Bağlantısı (Secrets üzerinden)
@st.cache_resource
def get_client():
    # Streamlit Secrets panelinden otomatik okur
    api_key = st.secrets.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)

client = get_client()

st.title("🧠 ATLAS | Dijital Sağ Kolum")
st.sidebar.header("🛠️ Yönetim Paneli")

# Görev Seçimi
gorev = st.sidebar.radio("Bir Görev Seçin:", ["İçerik Stratejisi", "Emlak İlanı"])

# Streaming Fonksiyonu (Daha Hızlı Yanıt)
def stream_ai_response(prompt):
    response = client.models.generate_content_stream(
        model='gemini-2.0-flash',
        contents=prompt
    )
    for chunk in response:
        yield chunk.text

# Görev 1: İçerik
if gorev == "İçerik Stratejisi":
    kategori = st.text_input("Kategori:")
    if st.button("Üret"):
        prompt = f"{kategori} kategorisi için Pinterest odaklı bir gelir stratejisi oluştur."
        with st.chat_message("assistant"):
            st.write_stream(stream_ai_response(prompt))

# Görev 2: Emlak
elif gorev == "Emlak İlanı":
    detay = st.text_area("Mülk Detayları:")
    if st.button("İlan Yaz"):
        prompt = f"Şu mülk için etkileyici bir ilan yaz: {detay}"
        with st.chat_message("assistant"):
            st.write_stream(stream_ai_response(prompt))