import streamlit as st
from PyPDF2 import PdfReader
import docx
import os
import io
import re

class ResumeParser:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, file_content):
        text = ''
        try:
            reader = PdfReader(io.BytesIO(file_content))
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            st.error("An error occurred while extracting text from PDF: {}".format(e))
            return text

    def extract_text_from_docx(self, file_content):
        text = ''
        try:
            doc = docx.Document(io.BytesIO(file_content))
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            return text
        except Exception as e:
            st.error("An error occurred while extracting text from DOCX: {}".format(e))
            return text

    def extract_contact_info(self, text):
        # Regular expressions for extracting phone numbers and email addresses
        phone_regex = r'\b(?:\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{4})\b'
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Extracting phone numbers
        phone_numbers = re.findall(phone_regex, text)
        # Extracting email addresses
        email_addresses = re.findall(email_regex, text)

        return phone_numbers, email_addresses

def main():
    st.title("Resume Parser")

    # File upload
    uploaded_file = st.file_uploader("Upload a resume file", type=["pdf", "docx"])

    if uploaded_file is not None:
        # Read the file
        file_content = uploaded_file.getvalue()
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        # Initialize the parser
        resume_parser = ResumeParser()

        if file_extension == ".pdf":
            text = resume_parser.extract_text_from_pdf(file_content)
        elif file_extension == ".docx":
            text = resume_parser.extract_text_from_docx(file_content)
        else:
            st.error("Unsupported file format. Please upload a PDF or DOCX file.")
            return

        # Extract contact information
        phone_numbers, email_addresses = resume_parser.extract_contact_info(text)

        # Display extracted text
        st.subheader("Extracted Text:")
        st.text(text)

        # Display contact information
        st.subheader("Extracted Contact Information:")
        st.write("Phone Numbers:", phone_numbers)
        st.write("Email Addresses:", email_addresses)

if __name__ == "__main__":
    main()
