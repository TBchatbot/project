import streamlit as st
import pandas as pd

st.set_page_config(page_title="Interactive AI TB Chatbot", layout="centered")
st.title("Interactive AI-Based Healthcare Chatbot for Tuberculosis")

url_who = "https://raw.githubusercontent.com/datasets/tuberculosis/main/data/tuberculosis.csv"
url_open_tb = "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/t/tb.csv"
url_xray_meta = "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/people/people-100.csv"

df_who = pd.read_csv(url_who)
df_open_tb = pd.read_csv(url_open_tb)
df_xray_meta = pd.read_csv(url_xray_meta)

user_input = st.text_input("Ask me anything about Tuberculosis (TB):")

def search_who(question):
    question = question.lower()
    if "cases" in question:
        recent = df_who[df_who['Year'] == df_who['Year'].max()]
        result = recent[['Country', 'New cases']]
        return "TB Cases (Latest Year):\n" + result.to_string(index=False)
    if "deaths" in question:
        recent = df_who[df_who['Year'] == df_who['Year'].max()]
        result = recent[['Country', 'Deaths']]
        return "TB Deaths (Latest Year):\n" + result.to_string(index=False)
    if "incidence" in question:
        recent = df_who[df_who['Year'] == df_who['Year'].max()]
        result = recent[['Country', 'Incidence']]
        return "TB Incidence (Latest Year):\n" + result.to_string(index=False)
    return ""

def search_open_tb(question):
    question = question.lower()
    if "notification" in question:
        recent = df_open_tb[df_open_tb['Year'] == df_open_tb['Year'].max()]
        result = recent[['Country', 'Notification']]
        return "TB Notifications (Latest Year):\n" + result.to_string(index=False)
    return ""

def general_info(question):
    q = question.lower()
    facts = {
        "symptoms": "Common symptoms: Cough > 2 weeks, fever, night sweats, weight loss, fatigue, chest pain, coughing blood.",
        "treatment": "TB is treatable with antibiotics over 6 months. DOTS is WHO recommended treatment strategy.",
        "prevention": "Prevent by avoiding close contact with infected people, vaccination (BCG), good ventilation.",
        "x-ray": "Chest X-ray is used for TB diagnosis, but requires expert analysis.",
        "cause": "TB is caused by Mycobacterium tuberculosis bacteria."
    }
    for k,v in facts.items():
        if k in q:
            return v
    return ""

if user_input:
    answer = search_who(user_input)
    if not answer:
        answer = search_open_tb(user_input)
    if not answer:
        answer = general_info(user_input)
    if not answer:
        answer = "Sorry, I don't have information on that. Please ask about TB cases, deaths, symptoms, treatment, prevention, or diagnostics."
    st.write(answer)

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
