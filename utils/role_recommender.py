def recommend_roles(resume_skills):
    skills = [skill.lower() for skill in resume_skills]
    roles = []

    if "python" in skills and "sql" in skills and ("power bi" in skills or "tableau" in skills):
        roles.append("Data Analyst")

    if "python" in skills and ("fastapi" in skills or "flask" in skills):
        roles.append("Backend Developer")

    if "python" in skills and ("machine learning" in skills or "ml" in skills):
        roles.append("Machine Learning Engineer")

    if "python" in skills and "c++" in skills:
        roles.append("Software Developer")

    if "power bi" in skills or "tableau" in skills:
        roles.append("BI Analyst")

    if not roles:
        roles.append("General Technical Associate")

    return roles