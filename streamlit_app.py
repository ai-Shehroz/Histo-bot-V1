import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Histopathology Report Generator", layout="centered")

# App title and header
st.markdown("## 🔬 Histopathology Report Generator")
st.markdown("### Developed by Shehroz Khan Rind")

# Input fields
patient_name = st.text_input("Patient Name")
age = st.text_input("Age")
sex = st.selectbox("Sex", ["Male", "Female", "Other"])
specimen = st.text_area("Specimen Details")
clinical = st.text_area("Clinical History")
gross = st.text_area("Gross Description")
microscopic = st.text_area("Microscopic Findings")

# Submit button
if st.button("Generate Report"):
    with st.spinner("Generating report..."):

        # Construct the prompt with gibberish input check
        prompt = f"""
You are an expert histopathologist. You are provided with sections of a histopathology case report.

Your job is to write a professional, accurate, and medically appropriate histopathology report using the input below.

If the provided input appears gibberish, nonsensical, or too short (e.g., less than a sentence), reply with:
"⚠️ Insufficient data provided to generate a histopathology report."

Input Details:
Patient Name: {patient_name}
Age: {age}
Sex: {sex}
Specimen Details: {specimen}
Clinical History: {clinical}
Gross Description: {gross}
Microscopic Findings: {microscopic}
"""

        # OpenRouter API call
        api_key = st.secrets["OPENROUTER_API_KEY"]
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            report = result["choices"][0]["message"]["content"]
            st.success("✅ Report generated successfully!")
            st.markdown("### 📝 Histopathology Report")
            st.markdown(report)
        else:
            st.error("❌ Failed to generate report. Please check your API key or input.")
