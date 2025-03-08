import streamlit as st
import fitz  # PyMuPDF
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

def preprocess_text(text):
    if not text:
        return set()
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    return set(words)

def calculate_ats_score(resume_text, job_desc_text):
    resume_words = preprocess_text(resume_text)
    job_desc_words = preprocess_text(job_desc_text)
    if not job_desc_words:
        return 0
    match_count = len(resume_words.intersection(job_desc_words))
    return round((match_count / len(job_desc_words)) * 100, 2) if job_desc_words else 0

def main():
    st.title("ATS Resume Filter")
    
    st.sidebar.header("Upload Your Resume")
    uploaded_file = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])
    
    st.sidebar.header("Paste Job Description")
    job_description = st.sidebar.text_area("Paste Job Description Here")
    
    if uploaded_file and job_description.strip():
        resume_text = extract_text_from_pdf(uploaded_file)
        if not resume_text.strip():
            st.error("Could not extract text from the uploaded PDF. Please try another file.")
            return
        ats_score = calculate_ats_score(resume_text, job_description)
        
        st.subheader("ATS Score")
        st.write(f"Your resume matches the job description with a score of **{ats_score}%**")
        
        if ats_score > 80:
            st.success("Your resume is highly relevant for this job!")
        elif ats_score > 50:
            st.warning("Your resume is somewhat relevant. Consider optimizing it.")
        else:
            st.error("Your resume needs significant improvements to match the job description.")

if __name__ == "__main__":
    main()
