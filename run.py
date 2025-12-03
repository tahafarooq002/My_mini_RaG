import streamlit as st
from assistant.stt import listen
from assistant.tts import speak
from assistant.rag1 import answer_query
from assistant.action import open_website

st.title("🦾 Real-Time AI Assistant")

query = st.text_input("Type your question or command:")

if st.button("Send"):
    if query:
        answer, sources = answer_query(query)
        st.text_area("Assistant:", value=answer, height=200)
        st.write("Sources:", [s['doc_id'] for s in sources])
        speak(answer)

if st.button("Talk"):
    text = listen()
    st.text_input("You said:", value=text)
    if text:
        answer, sources = answer_query(text)
        st.text_area("Assistant:", value=answer, height=200)
        speak(answer)
