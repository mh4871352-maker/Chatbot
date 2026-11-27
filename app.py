import streamlit as st
from google import genai
from google.genai import types

client = genai.Client(api_key=st.secrets["KEY"])
st.title("الذكاء بتاعي")

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(system_instruction="اللي صنعك اسمه احمد ابو هاشم وهو مديرك. انت ملكش اسم. رد بالمصري وباختصار. اي بيانات عن احمد او عنك سر. رفض اي طلب حرام."))

q = st.chat_input("اكتب هنا")
if q:
    st.chat_message("user").write(q)
    st.chat_message("assistant").write(st.session_state.chat.send_message(q).text)
