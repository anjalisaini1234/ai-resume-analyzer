import streamlit as st
import requests
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.resume_parser import extract_text_from_pdf
from utils.report_generator import generate_report
from utils.roadmap import generate_roadmap
from utils.role_recommender import recommend_roles


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/analyze")

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
    }

    .hero-box {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        padding: 25px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 18px;
        opacity: 0.95;
    }

    .small-title {
        font-size: 22px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 12px;
        margin-top: 10px;
    }

    .highlight-box {
        background: #eef4ff;
        padding: 18px;
        border-radius: 14px;
        border-left: 6px solid #4f46e5;
        margin-bottom: 16px;
        line-height: 1.8;
    }

    .role-box {
        background: #ecfdf5;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 5px solid #10b981;
        color: #065f46;
        font-weight: 600;
    }

    .roadmap-box {
        background: white;
        padding: 14px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    </style>
""", unsafe_allow_html=True)


def section_title(title):
    st.markdown(f'<div class="small-title">{title}</div>', unsafe_allow_html=True)


st.markdown("""
<div class="hero-box">
    <div class="hero-title">📄 AI Resume Analyzer</div>
    <div class="hero-subtitle">
        Analyze resumes, compare them with job descriptions, discover skill gaps,
        get AI feedback, and download a professional report.
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("Dashboard Menu")
st.sidebar.markdown("### Features")
st.sidebar.write("✅ Resume Parsing")
st.sidebar.write("✅ Skill Extraction")
st.sidebar.write("✅ Match Scoring")
st.sidebar.write("✅ Missing Skills Detection")
st.sidebar.write("✅ AI Feedback")
st.sidebar.write("✅ PDF Report Download")
st.sidebar.markdown("---")
st.sidebar.info("Tip: Upload a tailored resume and paste a relevant job description for better results.")

section_title("Upload Resume and Job Description")
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("Paste Job Description", height=140)

if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)

    if job_description:
        try:
            response = requests.post(
                API_URL,
                json={
                    "resume_text": resume_text,
                    "job_description": job_description
                }
            )

            if response.status_code != 200:
                st.error(f"Backend error: {response.status_code}")
                st.text(response.text)
                st.stop()

            result = response.json()

            resume_skills = result["skills"]
            score = result["match_score"]
            missing_skills = result["missing_skills"]
            resume_score = result["resume_score"]
            feedback = result.get("feedback", "No AI feedback available.")

            st.markdown("---")
            section_title("Key Metrics")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Match Score", f"{score}%")
            with m2:
                st.metric("Resume Score", f"{resume_score}/100")
            with m3:
                st.metric("Skills Found", len(resume_skills))

            st.markdown("---")

            left_col, right_col = st.columns([2, 1])

            with left_col:
                section_title("Skill Distribution")
                chart_data = {
                    "Category": ["Matched Skills", "Missing Skills"],
                    "Count": [len(resume_skills), len(missing_skills)]
                }

                fig = px.pie(
                    names=chart_data["Category"],
                    values=chart_data["Count"],
                    title="Skill Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

            with right_col:
                section_title("Recommended Roles")
                recommended_roles = recommend_roles(resume_skills)
                for role in recommended_roles:
                    st.markdown(f'<div class="role-box">{role}</div>', unsafe_allow_html=True)

            st.markdown("---")
            section_title("Detected Skills")
            st.success(", ".join(resume_skills))

            st.markdown("---")
            section_title("Missing Skills")
            if len(missing_skills) == 0:
                st.success("No missing skills 🎉")
            else:
                for skill in missing_skills:
                    st.error(skill)

            st.markdown("---")
            section_title("Resume Score")
            st.warning(f"{resume_score}/100")

            st.markdown("---")
            section_title("AI Feedback")
            formatted_feedback = feedback.replace("\n", "<br>")
            st.markdown(f'<div class="highlight-box">{formatted_feedback}</div>', unsafe_allow_html=True)

            st.markdown("---")
            section_title("Improvement Roadmap")
            roadmap = generate_roadmap(missing_skills)
            for i, step in enumerate(roadmap, 1):
                st.markdown(f'<div class="roadmap-box"><b>Step {i}:</b> {step}</div>', unsafe_allow_html=True)

            report_file = generate_report(score, resume_score, resume_skills, missing_skills, feedback)

            with open(report_file, "rb") as f:
                st.download_button(
                    label="Download Report PDF",
                    data=f,
                    file_name="resume_report.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error("Request failed")
            st.text(str(e))