import streamlit as st

st.title("🩺 AI-Based Healthcare Chatbot for Tuberculosis (TB)")

st.subheader("👤 Patient Details")
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=120)

st.subheader("😷 Symptoms Checker")
cough = st.checkbox("Persistent Cough")
fever = st.checkbox("Fever")
weight_loss = st.checkbox("Unexplained Weight Loss")
night_sweats = st.checkbox("Night Sweats")
fatigue = st.checkbox("Fatigue")

if st.button("🧪 Check TB Risk"):
    symptoms = [cough, fever, weight_loss, night_sweats, fatigue]
    symptom_count = sum(symptoms)

    if symptom_count >= 4:
        st.error(f"{name}, you are at **High Risk** of TB. Please consult a doctor immediately.")
    elif symptom_count >= 2:
        st.warning(f"{name}, you are at **Moderate Risk**. Monitor your symptoms and seek medical advice.")
    else:
        st.success(f"{name}, you are at **Low Risk**. Stay healthy and take precautions.")

with st.expander("ℹ️ About Tuberculosis (TB)"):
    st.write("""
    Tuberculosis (TB) is a contagious infection caused by bacteria.
    It mainly affects the lungs but can spread to other parts of the body.

    **Common Symptoms**:
    - Persistent cough (more than 2 weeks)
    - Fever
    - Weight loss
    - Night sweats
    - Fatigue

    **Prevention Tips**:
    - Early diagnosis and treatment
    - Vaccination (BCG)
    - Wearing masks
    - Avoiding close contact with infected individuals
    """)
