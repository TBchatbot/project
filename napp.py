import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI TB Chatbot", layout="centered")
st.title("AI-Based Healthcare Chatbot for Tuberculosis")

url_who = "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/tuberculosis.csv"
url_open_tb = "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/tb.csv"
url_xray_meta = "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/people-100.csv"

df_who = pd.read_csv(url_who)
df_open_tb = pd.read_csv(url_open_tb)
df_xray_meta = pd.read_csv(url_xray_meta)

def search_datasets(query):
    query_lower = query.lower()
    results = []
    if 'tb' in query_lower or 'tuberculosis' in query_lower:
        df_filtered = df_who[df_who.apply(lambda row: query_lower in str(row.values).lower(), axis=1)]
        if not df_filtered.empty:
            results.append("WHO Tuberculosis Data:\n" + df_filtered.head(5).to_string())
        df_filtered2 = df_open_tb[df_open_tb.apply(lambda row: query_lower in str(row.values).lower(), axis=1)]
        if not df_filtered2.empty:
            results.append("Open TB Dataset:\n" + df_filtered2.head(5).to_string())
    if 'xray' in query_lower or 'chest' in query_lower or 'image' in query_lower:
        results.append("Sample X-ray Metadata:\n" + df_xray_meta.head(5).to_string())
    if not results:
        results.append("No relevant data found for your query.")
    return "\n\n".join(results)

user_input = st.text_input("Ask any question about TB or related data:")

if user_input:
    answer = search_datasets(user_input)
    st.text_area("Answer", answer, height=300)

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

st.header("More TB Information")
st.markdown("""
- TB is caused by *Mycobacterium tuberculosis*.
- Spread through air via coughs/sneezes.
- Symptoms include prolonged cough, fever, weight loss, and night sweats.
- It is preventable and treatable.
- WHO recommends DOTS strategy for control.
