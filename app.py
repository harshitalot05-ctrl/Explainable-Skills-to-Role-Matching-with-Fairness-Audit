import streamlit as st
from src.skill_extraction import extract_skills
from src.role_recommendation import calculate_match
from src.explainability import get_explanation
import pandas as pd

roles = pd.read_csv("data/roles.csv")

st.title("Explainable Skills-to-Role Matching")

st.write("Paste your resume text below:")
uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["txt"]
)


if uploaded_file is not None:
    resume_text = uploaded_file.read().decode("utf-8")
else:
    resume_text = st.text_area("Resume")

if st.button("Analyze Resume"):

    skills = extract_skills(resume_text)

    st.subheader("Skills Found")

    if skills:
        st.write(skills)

        st.subheader("Role Matching")

        results = []

        for _, row in roles.iterrows():

            score, matched = calculate_match(
                skills,
                row["skills"]
            )

            results.append({
                "Role": row["role"],
                "Match Score (%)": score,
                "Matched Skills": ", ".join(matched)
            })

        results_df = pd.DataFrame(results)

        results_df = results_df.sort_values(
            "Match Score (%)",
            ascending=False
        )

        st.dataframe(results_df)

        best_role = results_df.iloc[0]

        st.success(
            f"🏆 Best Recommended Role: {best_role['Role']} "
            f"({best_role['Match Score (%)']}% match)"
        )

        # Get skills required by the recommended role
        role_skills = roles[
            roles["role"] == best_role["Role"]
        ].iloc[0]["skills"]

        # Generate explanation
        matched_skills, missing_skills = get_explanation(
            skills,
            role_skills
        )

        st.subheader("Why this role was recommended")

        st.write("✅ Matched Skills")
        st.write(matched_skills)

        st.write("❌ Missing Skills")
        st.write(missing_skills)

    else:
        st.warning("No skills found in the resume.")