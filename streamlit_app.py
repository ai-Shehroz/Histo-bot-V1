import streamlit as st
import requests
from datetime import datetime

# --- Streamlit Page Config ---
st.set_page_config(page_title="Histopathology Report Generator", page_icon="🧬", layout="wide")
st.markdown("<h1 style='text-align: center;'>🔬 Histopathology Report Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Developed by <strong>Shehroz Khan Rind</strong></p>", unsafe_allow_html=True)
st.markdown("---")

# --- API Key and Model ---
API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- Input Form ---
with st.form("histopathology_form"):
    st.subheader("🧑‍⚕️ Patient Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Patient Name")
    with col2:
        age = st.text_input("Age")
    with col3:
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])

    st.subheader("🧪 Specimen Details")
    specimen = st.text_input("Specimen Type / Biopsy Site")

    st.subheader("📋 Clinical History")
    clinical_history = st.text_area("Enter Clinical History")

    st.subheader("🧫 Gross Description")
    gross_description = st.text_area("Enter Gross Description")  # ✅ FIXED

    st.subheader("🔬 Microscopic Findings")
    microscopic_findings = st.text_area("Enter Microscopic Findings")

    submitted = st.form_submit_button("🧠 Generate Report")

# --- Generate Report ---
if submitted:
    with st.spinner("Generating report... Please wait"):
        prompt = f"""
You are a senior pathologist generating a detailed histopathology report.

Patient Name: {name}
Age: {age}
Sex: {sex}
Specimen: {specimen}
Clinical History: {clinical_history}
Gross Description: {gross_description}
Microscopic Findings: {microscopic_findings}

Generate a full report with proper medical language and structure. At the end, include a **Diagnosis section in bullet points**.
"""

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            result = response.json()

            if "choices" in result:
                report = result["choices"][0]["message"]["content"]

                st.success("✅ Report Generated Successfully")

                with st.expander("🧾 Full Histopathology Report", expanded=True):
                    st.text_area("View Report", report, height=400)

                if "Diagnosis" in report:
                    st.subheader("📌 Diagnosis Summary")
                    for line in report.splitlines():
                        if line.strip().startswith("-"):
                            st.markdown(f"✅ {line.strip()}")

                filename = f"{name.replace(' ', '_')}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                st.download_button(
                    label="⬇️ Download Report",
                    data=report,
                    file_name=filename,
                    mime="text/plain"
                )
            else:
                st.error("❌ Could not generate the report. Please check input.")
                st.json(result)

        except Exception as e:
            st.error(f"❌ API Error: {e}")
