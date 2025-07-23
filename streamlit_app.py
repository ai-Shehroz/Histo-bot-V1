import streamlit as st
import requests

st.set_page_config(page_title="Histopathology Report Generator", layout="centered")

# App Header
st.markdown(
    "<h1 style='text-align: center;'>🔬 Histopathology Report Generator</h1>"
    "<h4 style='text-align: center;'>Developed by Shehroz Khan Rind</h4><hr>",
    unsafe_allow_html=True,
)

# Input Fields
with st.form("report_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Patient Name")
        age = st.text_input("Age")
    with col2:
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        specimen = st.text_input("Specimen Details")

    clinical_history = st.text_area("Clinical History", height=100)
    gross_description = st.text_area("Gross Description", height=100)
    microscopic_findings = st.text_area("Microscopic Findings", height=100)

    submitted = st.form_submit_button("Generate Report")

if submitted:
    with st.spinner("Generating report..."):
        try:
            api_key = st.secrets["OPENROUTER_API_KEY"]
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "mistralai/mistral-7b-instruct:free",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a histopathologist. Generate a detailed report with diagnosis in bullet points from input.",
                        },
                        {
                            "role": "user",
                            "content": f"""
Patient Name: {name}
Age: {age}
Sex: {sex}
Specimen Details: {specimen}
Clinical History: {clinical_history}
Gross Description: {gross_description}
Microscopic Findings: {microscopic_findings}
""",
                        },
                    ],
                },
            )

            if response.status_code == 200:
                result = response.json()
                report = result["choices"][0]["message"]["content"]
                st.success("✅ Report generated successfully!")
                st.markdown("### 📝 Histopathology Report")
                st.write(report)
            else:
                st.error("❌ Could not generate the report. Please check input or API key.")
                st.json(response.json())
        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
