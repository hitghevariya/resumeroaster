#ai resume roaster
import streamlit as st
from dotenv import load_dotenv
import io
import os
import PyPDF2
import google.generativeai as genai

load_dotenv()
st.title("AI Resume Roaster")
st.divider()
st.badge("hey!")
st.markdown("Upload your resume and get AI powered roasting")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

uploaded_file = st.file_uploader("Upload your resume here (PDF and Text Only)",type=["pdf","txt"])
job_role = st.text_input("Enter JOB Role That You Are Targeting")

analyze = st.button("Analyze Resume")
print(analyze)

def extract_text_from_pdf(file_bytes):
    reader = PyPDF2.PdfReader(file_bytes)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text(uploaded_file):
    file_type = uploaded_file.type
    
    if file_type == "application/pdf":
        with io.BytesIO(uploaded_file.read()) as file_bytes:
            return extract_text_from_pdf(file_bytes)
        
    elif file_type == "text/plain":
        return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        file_content = extract_text(uploaded_file)
        
        if not file_content.strip():
            st.error("File does not have any content")
            st.stop()
            
        prompt = f"""
You are an experienced, brutally honest, no-nonsense HR professional with a sharp eye for resumes—and a sharper tongue. 
You’ve reviewed tens of thousands of resumes over the years, and you don’t sugarcoat feedback.

Now, your job is to roast the following resume with sarcasm, wit, and humor—but also offer real, helpful advice. 
The goal is to highlight what's wrong, what's missing, what's outdated, or what sounds like fluff, and then suggest ways to make it actually appealing for a {job_role} position at a reputable company.

Please:
- Be sharp and witty—don't hold back.
- Point out poor formatting, vague descriptions, irrelevant experience, clichés, and outdated skills.
- If the resume is too generic, boring, or lacking focus, say it.
- Keep the tone entertaining, but not offensive.
- Stay under 200 words.

Here is the resume:
--------------------
{file_content}
--------------------
Go ahead—roast it like it's your Monday morning coffee.
"""
        model = genai.GenerativeModel("models/gemini-1.5-flash")   
        response = model.generate_content(prompt)    
        st.markdown("Analsis Result")
        st.markdown(response.text)
    except Exception as e:
        st.error(f"An Error Occured")