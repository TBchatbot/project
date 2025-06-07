import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI TB Chatbot", layout="centered")
st.title("AI-Based Healthcare Chatbot for Tuberculosis")

if "history" not in st.session_state:
    st.session_state.history = []

url = "https://extranet.who.int/tme/generateCSV.asp?ds=estimates"
df = pd.read_csv(url)

def get_tb_info(country, question):
    country_data = df[df['country'].str.lower() == country.lower()]
    if country_data.empty:
        return "Sorry, no data found for this country."
    latest = country_data[country_data['year'] == country_data['year'].max()]
    if "cases" in question.lower():
        return f"TB cases in {country.title()}: {int(latest['e_inc_num'].values[0])}"
    if "deaths" in question.lower():
        return f"TB deaths in {country.title()}: {int(latest['e_mort_num'].values[0])}"
    return "Please ask about TB cases or deaths."

def check_symptoms(symptoms_text):
    symptoms_list = ["cough", "fever", "night sweats", "weight loss", "fatigue"]
    present = [s for s in symptoms_list if s in symptoms_text.lower()]
    if not present:
        return "No recognizable symptoms found. Please mention symptoms like cough, fever, night sweats, weight loss, or fatigue."
    risk_score = len(present) / len(symptoms_list) * 100
    if risk_score >= 60:
        return f"High Risk of TB based on symptoms: {risk_score:.0f}%"
    if risk_score >= 30:
        return f"Moderate Risk of TB based on symptoms: {risk_score:.0f}%"
    return f"Low Risk of TB based on symptoms: {risk_score:.0f}%"

user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input:
    st.session_state.history.append(("You", user_input))
    response = ""

    if user_input.lower().startswith("country:"):
        parts = user_input.split(" ", 1)
        if len(parts) > 1:
            country = parts[1].strip()
            response = f"Please ask your question about TB cases or deaths in {country}."
        else:
            response = "Please provide a country after 'country:'"
    elif user_input.lower().startswith("ask:"):
        parts = user_input.split(" ", 1)
        if len(parts) > 1:
            question = parts[1].strip()
            last_country = None
            for h in reversed(st.session_state.history):
                if h[0] == "You" and h[1].lower().startswith("country:"):
                    last_country = h[1].split(" ",1)[1].strip()
                    break
            if last_country:
                response = get_tb_info(last_country, question)
            else:
                response = "Please specify your country first using 'country: your_country'"
        else:
            response = "Please provide a question after 'ask:'"
    elif any(symptom in user_input.lower() for symptom in ["cough", "fever", "night sweats", "weight loss", "fatigue"]):
        response = check_symptoms(user_input)
    elif "upload x-ray" in user_input.lower():
        response = "Please use the upload widget below to upload your chest X-ray image."
    else:
        response = "Sorry, I didn't understand that. You can:\n- Specify your country by typing 'country: country_name'\n- Ask TB questions by typing 'ask: your question'\n- Describe symptoms\n- Type 'upload x-ray' to upload an image"

    st.session_state.history.append(("Bot", response))

for sender, msg in st.session_state.history:
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")

st.header("Chest X-ray Upload")
xray = st.file_uploader("Upload a chest X-ray image", type=['jpg', 'png'])
if xray:
    st.image(xray, caption="Uploaded X-ray", use_column_width=True)
    st.info("X-ray analysis feature coming soon")
