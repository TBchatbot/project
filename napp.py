import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="AI TB Healthcare Chatbot", layout="centered")
st.title("AI-Based Healthcare Chatbot for Tuberculosis")

url_who = "https://extranet.who.int/tme/generateCSV.asp?ds=estimates"
df_who = pd.read_csv(url_who)

url_open_tb = "https://query.data.world/s/kxghk53jq3wpzcvupzogflqmyjnyce"
df_open_tb = pd.read_csv(url_open_tb)

url_xray_meta = "https://raw.githubusercontent.com/datablist/sample-csv-files/main/files/people/people-100.csv"
df_xray_meta = pd.read_csv(url_xray_meta)

kb_texts = []

for idx, row in df_who.iterrows():
    kb_texts.append(f"In {row['country']} in {row['year']}, TB cases: {row['e_inc_num']}, deaths: {row['e_mort_num']}")

for idx, row in df_open_tb.iterrows():
    kb_texts.append(f"Data for {row['Country']}: TB prevalence {row['Prevalence']}")

kb_texts.append("Tuberculosis is caused by Mycobacterium tuberculosis and spreads through the air via coughs and sneezes.")
kb_texts.append("Symptoms include prolonged cough, fever, night sweats, weight loss, fatigue, chest pain, and coughing blood.")
kb_texts.append("TB is preventable and treatable. WHO recommends DOTS strategy for control.")
kb_texts.append("Chest X-ray images can help in TB diagnosis, but AI-based analysis is coming soon.")

model = SentenceTransformer('all-MiniLM-L6-v2')
kb_embeddings = model.encode(kb_texts, convert_to_tensor=True)

if "history" not in st.session_state:
    st.session_state.history = []

def get_response(user_message):
    user_emb = model.encode(user_message, convert_to_tensor=True)
    hits = util.semantic_search(user_emb, kb_embeddings, top_k=3)[0]
    answers = [kb_texts[hit['corpus_id']] for hit in hits]
    return "Here are some info related to your question:\n" + "\n".join(answers)

user_input = st.chat_input("Ask me anything about TB")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    response = get_response(user_input)
    st.session_state.history.append({"role": "assistant", "content": response})

for chat in st.session_state.history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["content"])
    else:
        st.chat_message("assistant").write(chat["content"])

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

[Learn More on WHO TB Page](https://www.who.int/teams/global-tuberculosis-programme)
""")
