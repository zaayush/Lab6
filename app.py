import streamlit as st
import openai
from PyPDF2 import PdfFileReader
from dotenv import load_dotenv

# Set your OpenAI API key
openai.api_key = "OPENAI_API_KEY"

# Function to extract text from PDF file
def extract_text_from_pdf(file):
    pdf_reader = PdfFileReader(file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text

# Function to generate cover letter
def generate_cover_letter(resume_text, job_description):
    prompt = f"Resume: {resume_text}\nJob Description: {job_description}\nGenerate a cover letter:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].text.strip()

# Main function
def main():
    # Check if session state exists, if not initialize it
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None

    # Upload resume PDF file
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

    if uploaded_file is not None:
        st.write("Resume Uploaded Successfully!")

        # Extract text from the PDF file
        resume_text = extract_text_from_pdf(uploaded_file)

        # Store resume text in session state
        st.session_state.resume_text = resume_text

    # Get job description
    job_description = st.text_input("Enter job description:")

    # Generate cover letter if both resume and job description are provided
    if st.session_state.resume_text is not None and job_description:
        cover_letter = generate_cover_letter(st.session_state.resume_text, job_description)
        st.write("Generated Cover Letter:")
        st.write(cover_letter)

if __name__ == "__main__":
    main()
