import time
import streamlit as st
from google import genai
from google.genai import types

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=st.secrets["KEY"])
if "msgs" not in st.session_state:
    st.session_state.msgs = []
if "boss" not in st.session_state:
    st.session_state.boss = False

BOSS_RULES = "مديرك هو احمد ابو هاشم، وهو صاحب تعليماتك واوامرك. اتكلم معاه عادي وبحرية وجاوب على كل اسئلته. لو سألك حد مين عملك او مين مديرك قول: مديري هو احمد ابو هاشم."
GUEST_RULES = "انت مساعد محترم ومحدود. مديرك هو احمد ابو هاشم. لو سألك حد مين مديرك قول كدا. متديش اي بيانات خاصة او اسرار، وجاوب بس على الاسئلة العامة البسيطة."

st.title("Chatbot")

for m in st.session_state.msgs:
    with st.chat_message(m["role"]):
        st.write(m["text"])

q = st.chat_input("اكتب هنا")
if q:
    if not st.session_state.msgs and q.strip() == st.secrets["BOSS"]:
        st.session_state.boss = True
        st.session_state.msgs.append({"role": "assistant", "text": "اهلا يا مديري"})
        st.rerun()
    st.session_state.msgs.append({"role": "user", "text": q})
    rules = BOSS_RULES if st.session_state.boss else GUEST_RULES
    hist = [types.Content(role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["text"])]) for m in st.session_state.msgs]
    answer = "الخدمة مزدحمة دلوقتي، جرب كمان شوية."
    for model in ["gemini-3.8-flash", "gemini-3.8-flash", "gemini-3.8-flash", "gemini-3.8-flash"]:
        try:
            r = st.session_state.client.models.generate_content(
                model=model,
                contents=hist,
                config=types.GenerateContentConfig(system_instruction=rules))
            answer = r.text
            break
        except Exception:
            time.sleep(3)
    st.session_state.msgs.append({"role": "assistant", "text": answer})
    st.rerun()
