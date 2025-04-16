import streamlit as st
from backend import get_patient_name, llm_chain
import json
from io import StringIO
import time

# Page config
st.set_page_config(page_title="Discharge Summary Generator", page_icon="🩺", layout="centered")

# Custom style for report container
st.markdown("""
    <style>
        .report-container {
            background-color: #f9f9f9;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("<h1>📝 Discharge Summary Generator</h1>", unsafe_allow_html=True)
st.markdown("Upload a `.json` file with patient data and optionally provide a prompt.")

uploaded_file = st.file_uploader("📂 Upload patient data in JSON format")

if uploaded_file is not None:
    
    try:
        # Extract patient name
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        patient_data = json.load(stringio)
        patient_name = get_patient_name(patient_data)
        # Show upload success
        st.markdown(f"### ✅ Data uploaded for **{patient_name}**")
        
        # Optional prompt
        st.markdown("#### 💬 Optionally, enter a prompt to customize the summary:")
        user_prompt = st.text_input("", key="prompt", placeholder="e.g., Emphasize mental health status or future care steps")

        # Button + Progress bar
        if st.button("Generate Summary"):
            with st.spinner("🧠 Generating summary..."):
                time.sleep(1)  # optional delay to show progress
                if user_prompt:
                    summary = llm_chain(patient_data, user_prompt)
                else:
                    summary = llm_chain(patient_data)

            # Show result in a styled container
            st.markdown("---")
            st.markdown("### 📋 Generated Discharge Summary")
            st.markdown(f"<div class='report-container'>{summary}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.markdown(f"{e}")
        st.markdown(f"### An error occurred. Try uploading a new file.")
