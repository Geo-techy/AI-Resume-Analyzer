from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
from dotenv import load_dotenv
import os
import re
import tempfile

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing from the environment.")

client = Groq(api_key=api_key)

# Initialize FastAPI App
app = FastAPI(title="AI Resume Analyzer API")

# Load the BERT model once
print("Loading BERT model into memory...")
ats_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
print("Model loaded successfully!")

# Helper Functions 

def calculate_similarity_bert(text1: str, text2: str) -> float:
    embeddings1 = ats_model.encode([text1])
    embeddings2 = ats_model.encode([text2])
    similarity = cosine_similarity(embeddings1, embeddings2)[0][0]
    return float(similarity)

def get_report(resume: str, job_desc: str) -> str:
    prompt = f"""
    # Context:
    - You are an AI Resume Analyzer, you will be given Candidate's resume and Job Description of the role he is applying for.

    # Instruction:
    - Analyze candidate's resume based on the possible points that can be extracted from job description,and give your evaluation on each point with the criteria below:  
    - Consider all points like required skills, experience,etc that are needed for the job role.
    - Calculate the score to be given (out of 5) for every point based on evaluation at the beginning of each point with a detailed explanation.  
    - If the resume aligns with the job description point, mark it with ✅ and provide a detailed explanation.  
    - If the resume doesn't align with the job description point, mark it with ❌ and provide a reason for it.  
    - If a clear conclusion cannot be made, use a ⚠️ sign with a reason.  
    - The Final Heading should be "Suggestions to improve your resume:" and give where and what the candidate can improve to be selected for that job role.

    # Inputs:
    Candidate Resume: {resume}
    ---
    Job Description: {job_desc}

    # Output:
    - Each any every point should be given a score (example: 3/5 ). 
    - Mention the scores and  relevant emoji at the beginning of each point and then explain the reason.
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content

def extract_scores(text: str):
    pattern = r'(\d+(?:\.\d+)?)/5'
    matches = re.findall(pattern, text)
    scores = [float(match) for match in matches]
    return scores

# API Endpoints 

@app.post("/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...), 
    job_desc: str = Form(...)
):
    if resume_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # 1. Save uploaded PDF to a temporary file to extract text
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await resume_file.read())
            tmp_path = tmp.name

        extracted_text = extract_text(tmp_path)
        os.remove(tmp_path) # Clean up temp file
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    # 2. Calculate ATS Similarity Score
    ats_score = calculate_similarity_bert(extracted_text, job_desc)

    # 3. Get LLM Report
    report = get_report(extracted_text, job_desc)

    # 4. Calculate Average LLM Score
    report_scores = extract_scores(report)
    avg_score = 0.0
    if report_scores:
        avg_score = sum(report_scores) / (5 * len(report_scores))

    # 5. Return JSON payload to Streamlit
    return {
        "similarity_score": ats_score,
        "average_score": avg_score,
        "report": report
    }
