import streamlit as st
from langdetect import detect
from googletrans import Translator

def translate_text(text, target_lang='en'):
    translator = Translator()
    return translator.translate(text, dest=target_lang).text

def detect_language(text):
    return detect(text)

def simple_tb_response(text):
    text = text.lower()
    if "symptom" in text:
        return "Common TB symptoms include cough, fever, night sweats, and weight loss."
    elif "treatment" in text:
        return "TB treatment usually involves a 6-month course of antibiotics."
    elif "cause" in text or "cause of tb" in text:
        return "TB is caused by the bacteria Mycobacterium tuberculosis."
    elif "prevent" in text or "prevention" in text:
        return "Prevention includes vaccination and avoiding close contact with infected people."
    else:
        return "Sorry, I can only answer questions about TB symptoms, causes, treatment, and prevention."

st.title("🩺 Simple TB Chatbot (No OpenAI)")

user_input = st.text_input("Ask me about Tuberculosis:")
if st.button("Send"):
    if user_input:
        lang = detect_language(user_input)
        translated_input = translate_text(user_input, 'en')
        response_en = simple_tb_response(translated_input)
        final_response = translate_text(response_en, lang)
        st.success(final_response)
