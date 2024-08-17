import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import os
import io
import base64

genai.configure(api_key="AIzaSyAWj21zza-Ydgk33TVMFbeU-IYh2lmB-Ck")

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open the PDF file using PyMuPDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        
        # Extract the first page as an image
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap()
        
        # Convert to bytes (PNG format)
        img_byte_arr = io.BytesIO()
        img_byte_arr.write(pix.tobytes(output="png"))
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/png",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit3 = st.button("Percentage match")

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match, if the resume matches
the job description. First the output should come as percentage, then keywords missing, and last, final thoughts.
"""

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
