import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()
openai_api_key = st.sidebar.text_input('Enter your OpenAI API Key and hit Enter', type="password")
genai.configure(api_key=openai_api_key)
def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

input_prompt = """
You are a skilled ATS(Application Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description.
Your evaluation should include:
- Percentage Match: How closely the resume matches the job description.
- Missing Keywords: List all keywords from the job description that are missing in the resume.
- Profile Summary: A brief summary of the candidate's profile based on the resume.
Ensure that all keywords mentioned in the job description are considered.
resume: {text}
description: {jd}

Provide the response in the format:
{
  "JD Match": "%",
  "MissingKeywords": [],
  "Profile Summary": ""
}
"""

st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)
    else:
        st.write("Please upload the resume")
