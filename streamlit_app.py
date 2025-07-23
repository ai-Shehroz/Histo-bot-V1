import streamlit as st
import requests

# App Header
st.set_page_config(page_title="🔬 Histopathology Report Generator", layout="wide")
st.title("🔬 Histopathology Report Generator Developed by Shehroz Khan Rind")

# Sidebar
st.sidebar.header("📝 Enter Patient Information")

# Patient Inputs
name = st.sidebar.text_input("Patient Name")
age = st.sidebar.text_input("Age")
sex = st.sidebar.selectbox("Sex", ["Male", "Female", "Other"])
specimen = st.sidebar.text_input("Specimen Details (e.g., Biopsy type)")
clinical_history = st.text_area("Clinical History")
gross_description = st.text_area("Gross Description")
microscopic_findings = st.text_area("Microscopic Findings")

# Generate Button
if st.button("🧾 Generate Report"):
    if all([name, age, sex, specimen, clinical_history, gross_description, microscopic_findings]):
        with st.spinner("Generating report..."):
            try:
                prompt = f"""
You are a senior histopathologist. Based on the following inputs, generate a professional histopathology report in markdown format.

Patient Name: {name}
Age: {age}
Sex: {sex}
Specimen Details: {specimen}
Clinical History: {clinical_history}
Gross Description: {gross_description}
Microscopic Findings: {microscopic_findings}

Include diagnosis as bullet points.
"""

                headers = {
                    "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                    "Content-Type": "application/json"
                }

                data = {
                    "model": "mistralai/mistral-7b-instruct:free",
                    "messages": [
                        {"role": "system", "content": "You are a professional histopathology report generator."},
                        {"role": "user", "content": prompt}
                    ]
                }

                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

                if response.status_code == 200:
                    result = response.json()
                    report = result['choices'][0]['message']['content']
                    st.markdown("### 🧠 Generated Report")
                    st.markdown(report)
                    st.success("✅ Report generated successfully!")
                else:
                    st.error("❌ Could not generate the report. Please check input or try again later.")
                    st.json(response.json())

            except Exception as e:
                st.error(f"❌ Could not generate the report.\n\n**Error:** {e}")
    else:
        st.warning("⚠️ Please fill in all the required fields before generating the report.")
