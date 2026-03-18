from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(score, resume_score, resume_skills, missing_skills, feedback):
    filename = "resume_report.pdf"
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Resume Analyzer Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Match Score: {score}%", styles["Normal"]))
    story.append(Paragraph(f"Resume Score: {resume_score}/100", styles["Normal"]))
    story.append(Paragraph(f"Detected Skills: {', '.join(resume_skills)}", styles["Normal"]))
    story.append(Paragraph(f"Missing Skills: {', '.join(missing_skills)}", styles["Normal"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("AI Feedback:", styles["Heading2"]))
    story.append(Paragraph(feedback.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(story)
    return filename