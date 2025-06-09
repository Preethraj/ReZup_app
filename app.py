import openai
import pdfplumber
import gradio as gr
from dotenv import load_dotenv

# SET YOUR GROQ API KEY
openai.api_key = "os.getenv("GROQ_API_KEY")"
openai.api_base = "https://api.groq.com/openai/v1"

def analyze_resume(text):
    prompt = f"""
    You are a professional resume reviewer. Analyze the following resume and provide constructive feedback, improvements, and suggestions:\n\n{text}
    """
    response = openai.ChatCompletion.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def review_resume(file):
    with pdfplumber.open(file.name) as pdf:
        resume_text = "".join([page.extract_text() for page in pdf.pages])
    return analyze_resume(resume_text)

gr.Interface(
    fn=review_resume,
    inputs="file",
    outputs="text",
    title="ReZup: Resume Uplifter"
).launch()
