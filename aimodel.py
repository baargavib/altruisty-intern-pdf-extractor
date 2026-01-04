import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Model name
GENAI_MODEL = "gemini-2.5-flash"

# Create the model object
model = genai.GenerativeModel(GENAI_MODEL)

def summarize_text(pdf_text):
    prompt = f"""
Summarize the following text clearly and concisely:

{pdf_text}
"""
    response = model.generate_content(prompt)
    return response.text

def extract_important_points(pdf_text):
    prompt = f"""
Extract the most important points from the following content.
Return them as bullet points.

Content:
{pdf_text}
"""
    response = model.generate_content(prompt)
    return response.text

def answer_question_from_document(doc_text, question):
    prompt = f"""
Answer the question strictly based on the content below.
If the answer is not present in the content, reply:
"Answer not found in the document."

Content:
{doc_text}

Question:
{question}
"""
    response = model.generate_content(prompt)
    return response.text
