import pandas as pd
import streamlit as st

st.title("WHO TB Estimates")

url = "https://extranet.who.int/tme/generateCSV.asp?ds=estimates"
df = pd.read_csv(url)

st.write("Global TB Data")
st.dataframe(df)

country = st.selectbox("Select a country", df['country'].unique())
country_data = df[df['country'] == country]
st.write(f"Data for {country}")
st.dataframe(country_data)
