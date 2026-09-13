def get_explanation(resume_skills, role_skills):

    resume_skills = set(resume_skills)

    role_skills = set(
        skill.strip().lower()
        for skill in role_skills.split(",")
    )

    matched_skills = resume_skills.intersection(role_skills)

    missing_skills = role_skills.difference(resume_skills)

    return list(matched_skills), list(missing_skills)