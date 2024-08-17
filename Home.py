from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Configure the Google Gemini API with the provided API key
genai.configure(api_key="AIzaSyAWj21zza-Ydgk33TVMFbeU-IYh2lmB-Ck")

def get_gemini_response(input, pdf_content, prompt):
    # Use the Gemini API to generate a response based on the input, PDF content, and prompt
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert the first page image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Prepare the PDF content for Gemini API
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App Configuration
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Input fields for job description and resume upload
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Button for percentage match functionality
submit3 = st.button("Percentage match")

# Prompt for percentage match
input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage, then the missing keywords, and finally, your final thoughts.
"""

if submit3:
    if uploaded_file is not None:
        try:
            # Process the uploaded PDF and get content
            pdf_content = input_pdf_setup(uploaded_file)
            # Get the response from the Gemini API
            response = get_gemini_response(input_prompt3, pdf_content, input_text)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.write("Please upload the resume")
