from fastapi import FastAPI
from pydantic import BaseModel

from utils.skill_extractor import extract_skills
from utils.similarity import calculate_similarity
from utils.skill_gap import find_missing_skills
from utils.resume_score import calculate_resume_score
from utils.ai_feedback import get_ai_feedback

app = FastAPI()

class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/analyze")
def analyze(data: ResumeRequest):
    resume_skills = extract_skills(data.resume_text)
    score = calculate_similarity(data.resume_text, data.job_description)
    missing_skills = find_missing_skills(data.resume_text, data.job_description)
    resume_score = calculate_resume_score(resume_skills, score)
    feedback = get_ai_feedback(data.resume_text)

    return {
        "skills": resume_skills,
        "match_score": score,
        "missing_skills": missing_skills,
        "resume_score": resume_score,
        "feedback": feedback
    }