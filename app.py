import streamlit as st
from google import genai
import os

# Sayfa Ayarları
st.set_page_config(page_title="ATLAS | Asistan", page_icon="🧠", layout="wide")

# Güvenli API Bağlantısı
@st.cache_resource
def get_client():
    # Secrets'tan anahtarı al
    api_key = st.secrets["GEMINI_API_KEY"]
    # Client'ı oluştur
    return genai.Client(api_key=api_key)

try:
    client = get_client()
except Exception as e:
    st.error(f"Bağlantı hatası: {e}")
    st.stop()

st.title("🧠 ATLAS | Dijital Sağ Kolum")
# ... (sidebar ve diğer kısımlar aynı kalabilir)

# Streaming Fonksiyonunu Güncelleyelim
def stream_ai_response(prompt):
    # 'gemini-1.5-flash' genelde daha yüksek başarı oranına sahiptir
    response = client.models.generate_content_stream(
        model='gemini-1.5-flash',
        contents=prompt
    )
    for chunk in response:
        # chunk.text'in boş gelme ihtimaline karşı kontrol
        if chunk.text:
            yield chunk.text

# İçerik ve Emlak kısımlarını kodundaki gibi bırak...