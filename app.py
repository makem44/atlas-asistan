import streamlit as st
from google import genai

# Sayfa ayarları
st.set_page_config(page_title="ATLAS", layout="wide")

# Güvenli bağlantı
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
    st.sidebar.success("Sistem Bağlantısı Başarılı!")
except Exception as e:
    st.sidebar.error("API Anahtarı hatası!")
    st.stop()

st.title("🧠 ATLAS | Dijital Sağ Kolum")

# Streaming fonksiyonu - Hata yönetimi eklenmiş
def stream_ai_response(prompt):
    try:
        # Model adını değiştirebilirsin: 'gemini-1.5-flash' genelde en hızlısıdır.
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
gorev = st.sidebar.radio("Görev Seç:", ["İçerik Stratejisi", "Emlak İlanı"])

if gorev == "İçerik Stratejisi":
    kategori = st.text_input("Kategori:")
    if st.button("Üret"):
        with st.chat_message("assistant"):
            st.write_stream(stream_ai_response(f"{kategori} için Pinterest içerik stratejisi yaz."))

elif gorev == "Emlak İlanı":
    detay = st.text_area("Mülk Detayları:")
    if st.button("İlan Yaz"):
        with st.chat_message("assistant"):
            st.write_stream(stream_ai_response(f"Şu mülk için etkileyici bir emlak ilanı yaz: {detay}"))
