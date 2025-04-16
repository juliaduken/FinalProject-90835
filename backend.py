import openai
from openai import OpenAI
import json
import logging

### logging ###
# Configure logging
logging.basicConfig(
    filename='interactions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

### credentials ###
# load the credentials
credentials_path = 'credentials.json'
with open(credentials_path, 'r') as file:
    credentials = json.load(file)

# extract OPENAI API key
openai_api_key = credentials['openai_api_key']
openai.api_key = openai_api_key

### helpers ###
# get patient name
def get_patient_name(data):
    patient_name = data['patient_demographics']['name']
    return patient_name

# get patient diagnosis
def get_patient_diagnosis(data):
    patient_diagnosis = data['diagnoses'][0]['description']
    return patient_diagnosis

# remove PHI from data
def clean_data(data):
    if "patient_id" and "patient_demographics" in data:
        del data["patient_id"]
        del data["patient_demographics"]
        return data

### prompts ###
### prompt 1 -> research diagnosis
def research_prompt(diagnosis):

    client = OpenAI(api_key=openai_api_key)
    prompt = f"""
    You will first receive a diagnosis.

    Diagnosis: {diagnosis}
    
    Then, I want you to research the following: The diagnosis, what important tests and/or bloodwork are relevant, and most importantly, 
    identify the most important information to glean from a patient's data if it is available to write an effective discharge summary.
    
    After your research, I want you to return your list of summarized criteria that is important to obtain from a patient's data if it
    were to be available.
    """ 

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4",
    )

    logging.info("Research prompt:\n%s", prompt) 

    response = chat_completion.choices[0].message.content
    logging.info("✅ Research response:\n%s", response)

    return response

### prompt 2 -> gen discharge summary
def summarize_prompt(patient_data, diagnosis_research, user_prompt=None):
    client = OpenAI(api_key=openai_api_key)
    
    prompt = f"""
    You will receive a .json file containing patient data. 

    Your task is to use this above data to write a thorough discharge summary. 
    
    You should be sure to include all of the following information, if available:
    {diagnosis_research}

    Your summary should include at the very minimum: a reason for admission, diagnosis,
    and a description of the course of the hospital stay, paying careful consideration to the order
    and timing of different aspects of treatment. 

    Do not include any sections of information if it is not given. Do not include additional notes regarding limitations of data or this being for instructional purposes.
    
    Patient Data: {patient_data}
    
    Additionally, consider the following instructions if available (will display "None" if not available)
    Additional information: {user_prompt}
    """ 

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4",
    )

    logging.info("Summary prompt:\n%s", prompt) 

    response = chat_completion.choices[0].message.content
    logging.info("✅ Summary response:\n%s", response)

    return response

def llm_chain(patient_data, user_prompt=None):
    patient_diagnosis = get_patient_diagnosis(patient_data)
    logging.info("Extracted diagnosis: %s", patient_diagnosis)
    patient_data = clean_data(patient_data)
    logging.info("Removed PHI from patient data: %s", patient_data)
    research = research_prompt(patient_diagnosis)
    if user_prompt:
        summary = summarize_prompt(patient_data, research, user_prompt)
    else:
        summary = summarize_prompt(patient_data, research)
    return summary