import streamlit as st
from google import genai
import time

st.set_page_config(page_title="ATLAS | Asistan", page_icon="🧠", layout="wide")

# API İstemcisini oluştur
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Anahtarı hatası!")
    st.stop()

st.title("🧠 ATLAS | Dijital Sağ Kolum")

# Streaming fonksiyonu (Daha kararlı yapı)
def stream_ai_response(prompt):
    try:
        # İsteği gönder
        response = client.models.generate_content_stream(
            model='gemini-1.5-flash',
            contents=prompt
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"Hata oluştu: {str(e)}"

# Arayüz
kategori = st.text_input("Kategori girin:")
if st.button("Üret"):
    if kategori:
        with st.chat_message("assistant"):
            # st.write_stream kullanırken yanıtı izle
            st.write_stream(stream_ai_response(f"{kategori} için Pinterest stratejisi yaz."))
    else:
        st.warning("Lütfen bir kategori girin.")
