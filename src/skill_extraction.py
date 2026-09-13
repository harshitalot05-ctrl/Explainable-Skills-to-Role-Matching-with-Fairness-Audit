SKILLS = [
    "python",
    "sql",
    "excel",
    "power bi",
    "statistics",
    "pandas",
    "numpy",
    "machine learning",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "git",
    "java",
    "oop",
    "data structures",
    "communication",
    "business analysis"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills