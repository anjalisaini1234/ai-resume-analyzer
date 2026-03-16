def generate_suggestions(resume_text, missing_skills):

    suggestions = []

    text = resume_text.lower()

    # Suggest missing skills
    if len(missing_skills) > 0:
        suggestions.append(
            "Consider learning or adding these skills: " + ", ".join(missing_skills)
        )

    # Check for projects
    if "project" not in text:
        suggestions.append("Add project experience to strengthen your resume.")

    # Check for GitHub
    if "github" not in text:
        suggestions.append("Include your GitHub profile to showcase projects.")

    # Check for achievements
    if "achieved" not in text and "improved" not in text:
        suggestions.append("Add measurable achievements (e.g., improved accuracy by 20%).")

    return suggestions