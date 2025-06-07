import streamlit as st
import pandas as pd

df = pd.read_csv('your_tb_dataset.csv')

def answer_question(question):
    question = question.lower()
    matched_rows = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(question).any(), axis=1)]
    if matched_rows.empty:
        return "Sorry, no data found related to your question."
    else:
        return matched_rows.head(3).to_string(index=False)

print("Ask me anything about Tuberculosis. Type 'exit' to quit.")
while True:
    q = input("Your question: ")
    if q.strip().lower() == 'exit':
        break
    print(answer_question(q))
    print()


st.set_page_config(page_title="AI TB Chatbot", layout="centered")
st.title("AI-Based Healthcare Chatbot for Tuberculosis")

url = "https://extranet.who.int/tme/generateCSV.asp?ds=estimates"
df = pd.read_csv(url)

country = st.text_input("Enter your country:")
question = st.text_input("Ask about TB cases or deaths in the country:")

if country and question:
    country_data = df[df['country'].str.lower() == country.lower()]
    if not country_data.empty:
        latest = country_data[country_data['year'] == country_data['year'].max()]
        if "cases" in question.lower():
            st.success(f"TB cases in {country.title()}: {int(latest['e_inc_num'].values[0])}")
        elif "deaths" in question.lower():
            st.success(f"TB deaths in {country.title()}: {int(latest['e_mort_num'].values[0])}")
        else:
            st.info("Try asking about TB cases or deaths")

st.header("Symptom Checker")
cough = st.checkbox("Cough lasting more than 2 weeks")
fever = st.checkbox("Fever")
night_sweats = st.checkbox("Night sweats")
weight_loss = st.checkbox("Weight loss")
fatigue = st.checkbox("Fatigue")

symptoms = [cough, fever, night_sweats, weight_loss, fatigue]
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
