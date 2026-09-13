import streamlit as st
from src.skill_extraction import extract_skills
from src.resume_parser import extract_text_from_file
from src.role_recommendation import calculate_match
from src.explainability import get_explanation
import pandas as pd
import plotly.express as px


# Load job roles
roles = pd.read_csv("data/roles.csv")


# Page title
st.title("Explainable Skills-to-Role Matching")

st.write("Paste your resume text below:")


# Resume upload
uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["txt", "pdf", "docx"]
)


# Read resume
if uploaded_file is not None:

    resume_text = extract_text_from_file(uploaded_file)

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=200
    )

else:

    resume_text = st.text_area("Resume")


# Analyze button
if st.button("Analyze Resume"):

    # Extract skills
    skills = extract_skills(resume_text)

    st.subheader("Skills Found")

    if skills:

        st.write(skills)

        # Role matching
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


        # Create results table
        results_df = pd.DataFrame(results)


        # Sort by match score
        results_df = results_df.sort_values(
            "Match Score (%)",
            ascending=False
        )


        # Display table
        st.dataframe(results_df)


        # Match score chart
        st.subheader("Role Match Scores")

        fig = px.bar(
            results_df,
            x="Role",
            y="Match Score (%)",
            title="Resume Match Score by Role"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # Best role
        best_role = results_df.iloc[0]

        st.success(
            f"🏆 Best Recommended Role: "
            f"{best_role['Role']} "
            f"({best_role['Match Score (%)']}% match)"
        )


        # Get skills required by recommended role
        role_skills = roles[
            roles["role"] == best_role["Role"]
        ].iloc[0]["skills"]


        # Generate explanation
        matched_skills, missing_skills = get_explanation(
            skills,
            role_skills
        )


        # Explanation
        st.subheader("Why this role was recommended")


        st.write("✅ Matched Skills")
        st.write(matched_skills)


        st.write("❌ Missing Skills")
        st.write(missing_skills)


    else:

        st.warning(
            "No skills found in the resume."
        )

        # Fairness Audit
st.subheader("⚖️ Fairness Audit")

fairness_data = pd.read_csv("data/fairness_eval.csv")

group_a_scores = fairness_data[
    fairness_data["Group"] == "Group_A"
]["Match_Score"].tolist()

group_b_scores = fairness_data[
    fairness_data["Group"] == "Group_B"
]["Match_Score"].tolist()

average_a = sum(group_a_scores) / len(group_a_scores)
average_b = sum(group_b_scores) / len(group_b_scores)

fairness_gap = abs(average_a - average_b)

st.write(
    f"Average Match Score - Group A: {average_a:.2f}%"
)

st.write(
    f"Average Match Score - Group B: {average_b:.2f}%"
)

st.write(
    f"Fairness Gap: {fairness_gap:.2f} percentage points"
)

if fairness_gap <= 5:
    st.success("✅ Low difference between the two groups.")
elif fairness_gap <= 10:
    st.warning("⚠️ Moderate difference between the two groups.")
else:
    st.error("🚨 High difference between the two groups.")