import streamlit as st
from utils.suggestions import generate_suggestions
from utils.resume_score import calculate_resume_score
from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.similarity import calculate_similarity
from utils.skill_gap import find_missing_skills

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer & Job Match System")
st.markdown("Upload your resume and compare it with a job description.")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("Paste Job Description")

if uploaded_file is not None:

    resume_text = extract_text_from_pdf(uploaded_file)

    resume_skills = extract_skills(resume_text)

    st.subheader("Detected Skills")
    st.success(", ".join(resume_skills))

    if job_description:

        score = calculate_similarity(resume_text, job_description)

        st.subheader("Job Match Score")
        st.success(f"{score}% Match")

        missing_skills = find_missing_skills(resume_text, job_description)

        st.subheader("Missing Skills")

        if len(missing_skills) == 0:
            st.success("No missing skills 🎉 Your resume matches the job well.")
        else:
            st.write(missing_skills)

        resume_score = calculate_resume_score(resume_skills, score)

        st.subheader("Resume Score")
        st.info(f"{resume_score} / 100")
        suggestions = generate_suggestions(resume_text, missing_skills)

        st.subheader("Resume Suggestions")

        for suggestion in suggestions:
            st.write("•", suggestion)