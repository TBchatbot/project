import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI TB Chatbot", layout="centered")
st.title("AI-Based Healthcare Chatbot for Tuberculosis")

url_who = "https://raw.githubusercontent.com/datasets/tb/master/data/tb.csv"
url_open_tb = "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/tb/tb_2016.csv"
url_xray_meta = "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/people/people-100.csv"

df_who = pd.read_csv(url_who)
df_open_tb = pd.read_csv(url_open_tb)
df_xray_meta = pd.read_csv(url_xray_meta)

knowledge = []
for col in df_who.columns:
    knowledge.append(f"WHO TB Data {col}: " + ", ".join(df_who[col].astype(str).unique()))
for col in df_open_tb.columns:
    knowledge.append(f"Open TB Data {col}: " + ", ".join(df_open_tb[col].astype(str).unique()))
knowledge.append("Tuberculosis is caused by Mycobacterium tuberculosis.")
knowledge.append("Symptoms include prolonged cough, fever, night sweats, weight loss, fatigue, chest pain, and coughing blood.")
knowledge.append("TB is preventable and treatable with proper medical care.")
knowledge.append("WHO recommends DOTS strategy for TB control.")

vectorizer = TfidfVectorizer().fit_transform(knowledge)

user_question = st.text_input("Ask me anything about Tuberculosis:")

if user_question:
    q_vec = TfidfVectorizer().fit(knowledge).transform([user_question])
    sims = cosine_similarity(q_vec, vectorizer).flatten()
    max_sim_idx = sims.argmax()
    answer = knowledge[max_sim_idx]
    st.write("Answer:", answer)

st.header("Symptom Checker")
cough = st.checkbox("Cough lasting more than 2 weeks")
fever = st.checkbox("Fever")
night_sweats = st.checkbox("Night sweats")
weight_loss = st.checkbox("Weight loss")
fatigue = st.checkbox("Fatigue")
chest_pain = st.checkbox("Chest pain")
blood_cough = st.checkbox("Coughing blood")
symptoms = [cough, fever, night_sweats, weight_loss, fatigue, chest_pain, blood_cough]
risk_score = sum(symptoms) / len(symptoms) * 100
if st.button("Calculate TB Risk"):
    if risk_score >= 60:
        st.warning(f"High Risk: {risk_score:.0f}%")
    elif risk_score >= 30:
        st.info(f"Moderate Risk: {risk_score:.0f}%")
    else:
        st.success(f"Low Risk: {risk_score:.0f}%")

st.header("Upload Chest X-ray")
xray = st.file_uploader("Upload a chest X-ray image", type=['jpg', 'png'])
if xray:
    st.image(xray, caption="Uploaded X-ray", use_column_width=True)
    st.info("X-ray analysis feature coming soon")

st.header("Sample X-ray Dataset Metadata")
st.dataframe(df_xray_meta.head())
