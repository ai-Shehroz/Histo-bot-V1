import streamlit as st
import openai

# Load API key from secrets.toml
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"

st.set_page_config(page_title="Histopathology Report Generator", layout="centered")

st.markdown("<h1 style='text-align: center;'>🔬 Histopathology Report Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Developed by Shehroz Khan Rind</h4>", unsafe_allow_html=True)
st.markdown("---")

# Input fields
with st.form("report_form"):
    st.subheader("📄 Patient Information")
    name = st.text_input("Patient Name")
    age = st.text_input("Age")
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])

    st.subheader("🧪 Specimen Details")
    specimen = st.text_area("Type and Source of Specimen")

    st.subheader("🩺 Clinical History")
    clinical_history = st.text_area("Clinical History")

    st.subheader("🧬 Gross Description")
    gross_description = st.text_area("Gross Description")

    st.subheader("🔬 Microscopic Findings")
    microscopic_findings = st.text_area("Microscopic Findings")

    submit = st.form_submit_button("🧾 Generate Report")

if submit:
    if not all([name, age, sex, specimen, clinical_history, gross_description, microscopic_findings]):
        st.error("❌ Please fill all the fields.")
    else:
        with st.spinner("Generating report..."):

            prompt = f"""
You are an expert histopathologist. Generate a detailed histopathology report using the following information:

Patient Name: {name}
Age: {age}
Sex: {sex}

Specimen: {specimen}
Clinical History: {clinical_history}
Gross Description: {gross_description}
Microscopic Findings: {microscopic_findings}

Provide the final report with a clear diagnosis (in bullet points if possible), and write in a formal medical tone.
"""

            try:
                response = openai.ChatCompletion.create(
                    model="mistralai/mistral-7b-instruct:free",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                report = response.choices[0].message.content.strip()
                st.success("✅ Report generated successfully!")
