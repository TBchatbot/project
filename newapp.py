import streamlit as st
from langdetect import detect
from googletrans import Translator
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

translator = Translator()

def translate_text(text, target_lang='en'):
    return translator.translate(text, dest=target_lang).text

def detect_language(text):
    return detect(text)

def get_llm_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful TB healthcare assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def tb_chatbot(user_input):
    lang = detect_language(user_input)
    translated = translate_text(user_input, 'en')
    llm_reply = get_llm_response(translated)
    final_reply = translate_text(llm_reply, lang)
    return final_reply

st.title("🩺 Multilingual TB Chatbot")
user_input = st.text_input("Ask me anything about Tuberculosis:")
if st.button("Send"):
    if user_input:
        reply = tb_chatbot(user_input)
        st.success(reply)
