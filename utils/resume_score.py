def calculate_resume_score(resume_skills, match_score):

    score = 0

    # Skills score
    skill_score = min(len(resume_skills) * 5, 40)

    # Job match score
    match_score_component = match_score * 0.4

    score = skill_score + match_score_component

    if score > 100:
        score = 100

    return round(score, 2)