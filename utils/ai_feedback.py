import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

def fallback_feedback(resume_text: str) -> str:
    text = resume_text.lower()

    strengths = []
    improvements = []

    if "python" in text:
        strengths.append("Good Python knowledge is visible in the resume.")
    if "sql" in text:
        strengths.append("SQL skill adds value for analyst and backend-related roles.")
    if "power bi" in text or "tableau" in text:
        strengths.append("You have reporting and dashboard skills, which are useful for analyst roles.")
    if "c++" in text:
        strengths.append("C++ shows programming fundamentals and problem-solving ability.")

    if "aws" not in text:
        improvements.append("Add cloud exposure such as AWS, Azure, or GCP.")
    if "fastapi" not in text and "flask" not in text:
        improvements.append("Add backend/API project experience using FastAPI or Flask.")
    if "docker" not in text:
        improvements.append("Mention deployment or containerization tools like Docker.")
    if "github" not in text:
        improvements.append("Add Git/GitHub project collaboration details.")
    if "machine learning" not in text and "ml" not in text:
        improvements.append("Add at least one machine learning project with metrics and deployment.")

    if not strengths:
        strengths.append("Your resume shows technical learning potential, but it can be made stronger with clearer project impact.")

    if not improvements:
        improvements.append("Your profile looks balanced. Add quantified project results to improve it further.")

    feedback = "Strengths:\n"
    for s in strengths:
        feedback += f"- {s}\n"

    feedback += "\nSuggestions for Improvement:\n"
    for i in improvements:
        feedback += f"- {i}\n"

    return feedback


def get_ai_feedback(resume_text: str) -> str:
    if not api_key:
        return fallback_feedback(resume_text)

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""
Analyze this resume and provide:
1. Strengths
2. Weaknesses
3. Missing skills
4. Suggestions for improvement

Resume:
{resume_text}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception:
        return fallback_feedback(resume_text)