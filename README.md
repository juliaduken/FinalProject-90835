# 🩺 Discharge Summary Generator

This Streamlit-based web application uses OpenAI's GPT-4 to automatically generate detailed patient discharge summaries from JSON-formatted patient data.

## Project Overview

This project was developed for a class assignment to demonstrate the integration of large language models (LLMs) in healthcare applications. Sample patient data is provided in `.json` format and is uploaded through the Streamlit interface.

The app:
- Extracts the patient name and diagnosis
- Uses GPT-4 to research relevant clinical information for the diagnosis
- Generates a tailored discharge summary based on provided patient data
- Optionally incorporates user instructions (e.g., "focus on mental health")

---

## Features

- Upload patient data in JSON format
- Automatically extract patient name
- GPT-powered diagnosis research
- Customizable discharge summary with optional prompt
- Progress bar during summary generation
- Styled summary display in the app
- Logging of all interactions (`interactions.log`)
- Easy to run locally

---

## File Structure

```
├── app.py                 # Main Streamlit app
├── backend.py             # Helper functions and OpenAI prompt logic
├── credentials.json       # API key (user-provided; excluded via .gitignore)
├── .gitignore             # Ignores virtual environments, logs, and credentials
├── requirements.txt       # Install these requirements to run the program
├── interactions.log       # Generated log of prompt interactions (auto-created)
└── README.md              # You are here!
```

---

## Requirements

- Python 3.8+
- Streamlit
- OpenAI Python SDK

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Setup Instructions

1. Clone the repository.
2. Create a file named `credentials.json` in the project root with the following format:

```json
{
  "openai_api_key": "your-openai-api-key-here"
}
```

**Do not share this file publicly.** It is excluded from version control using `.gitignore`.

3. Run the app locally:

```bash
streamlit run app.py
```

---

## Example Input Format

The uploaded `.json` file must include at least:

```json
{
  "patient_demographics": {
    "name": "John Doe"
  },
  "diagnoses": [
    {
      "description": "Pneumonia"
    }
  ],
  ...
}
```

More fields are used by the language model but can vary.

---

## Logging

All prompt interactions are logged in `interactions.log`, including:
- Research prompts
- Summary prompts
- GPT responses

---

## Powered By

- [OpenAI GPT-4](https://platform.openai.com/)
- [Streamlit](https://streamlit.io/)

---

## Authors

Developed as part of a Spring 2025 AI course at Carnegie Mellon University.

---

## Notes

- Only meant for local deployment.
- For demonstration purposes only — not for use in actual clinical environments.
- ChatGPT was utilized to help write this README file.

---

