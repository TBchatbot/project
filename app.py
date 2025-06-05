import streamlit as st
from transformers import pipeline

chatbot = pipeline("text-generation", model="gpt2")

st.title("🩺 TB Healthcare Chatbot")

q = st.text_input("Ask me about Tuberculosis:")
if st.button("Send"):
    if q:
        a = chatbot(q, max_length=100)[0]['generated_text']
        st.success(a)
