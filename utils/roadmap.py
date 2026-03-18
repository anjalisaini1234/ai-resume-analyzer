def generate_roadmap(missing_skills):
    if not missing_skills:
        return [
            "Improve project descriptions with measurable impact.",
            "Add deployment links and GitHub links.",
            "Customize resume for each application."
        ]

    roadmap = []
    for skill in missing_skills:
        roadmap.append(f"Learn or strengthen {skill}.")
        roadmap.append(f"Build one mini project using {skill}.")
        roadmap.append(f"Add {skill} clearly in projects or skills section if you already know it.")
    return roadmap[:6]