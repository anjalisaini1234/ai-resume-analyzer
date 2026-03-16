import re

skills_database = [
    "python",
    "java",
    "c++",
    "sql",
    "machine learning",
    "deep learning",
    "data analysis",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "power bi",
    "tableau",
    "aws",
    "docker",
    "kubernetes",
    "html",
    "css",
    "javascript",
    "react"
]

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_database:
        if re.search(skill, text):
            found_skills.append(skill)

    return found_skills