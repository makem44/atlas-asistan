import streamlit as st
from google import genai

# 1. Sayfa Ayarları
st.set_page_config(page_title="ATLAS", layout="wide")

# 2. Bağlantı (Hata mesajını detaylı görelim)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    st.sidebar.success("Sistem Bağlantısı Başarılı!")
except Exception as e:
    st.sidebar.error(f"Anahtar hatası: {e}")
    st.stop()

st.title("🧠 ATLAS | Dijital Sağ Kolum")

# 3. Streaming Fonksiyonu (Hata yakalama eklenmiş)
def stream_ai_response(prompt):
    try:
        # Model adını 'gemini-1.5-flash' olarak tutuyoruz
        response = client.models.generate_content_stream(
            model='gemini-1.5-flash', 
            contents=prompt
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"API Hatası: {str(e)}"

# 4. Arayüz
gorev = st.sidebar.radio("Görev Seç:", ["İçerik Stratejisi", "Emlak İlanı"])

if gorev == "İçerik Stratejisi":
    kategori = st.text_input("Kategori:")
    if st.button("Üret"):
        with st.chat_message("assistant"):
            st.write_stream(stream_ai_response(f"{kategori} için Pinterest içerik stratejisi yaz."))
