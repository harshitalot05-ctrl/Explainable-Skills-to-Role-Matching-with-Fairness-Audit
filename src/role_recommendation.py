def calculate_match(resume_skills, role_skills):
    resume_skills = set(resume_skills)
    role_skills = set(skill.strip().lower() for skill in role_skills.split(","))

    matched_skills = resume_skills.intersection(role_skills)

    if len(role_skills) == 0:
        score = 0
    else:
        score = (len(matched_skills) / len(role_skills)) * 100

    return round(score, 2), list(matched_skills)