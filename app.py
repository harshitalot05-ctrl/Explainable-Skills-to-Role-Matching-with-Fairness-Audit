import streamlit as st
from src.skill_extraction import extract_skills
from src.resume_parser import extract_text_from_file
from src.role_recommendation import calculate_match
from src.explainability import get_explanation
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Skills-to-Role Matching",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }

    h1 {
        font-size: 2.5rem;
        font-weight: 700;
    }

    h2, h3 {
        font-weight: 600;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD JOB ROLES
# ============================================================

roles = pd.read_csv("data/roles.csv")


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🎯 Explainable Skills-to-Role Matching")

st.markdown(
    "### Resume Analysis • Role Recommendation • Explainability • Fairness Audit"
)

st.divider()


# ============================================================
# RESUME INPUT
# ============================================================

st.write("Upload your resume or paste your resume text below:")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["txt", "pdf", "docx"]
)


# ============================================================
# READ RESUME
# ============================================================

if uploaded_file is not None:

    resume_text = extract_text_from_file(uploaded_file)

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=200
    )

else:

    resume_text = st.text_area(
        "Resume",
        height=200
    )


# ============================================================
# ANALYZE RESUME
# ============================================================

if st.button("Analyze Resume"):

    # --------------------------------------------------------
    # EXTRACT SKILLS
    # --------------------------------------------------------

    skills = extract_skills(resume_text)

    if skills:

        # ----------------------------------------------------
        # SKILLS FOUND
        # ----------------------------------------------------

        st.subheader("🧠 Skills Found")

        st.write(skills)


        # ----------------------------------------------------
        # ROLE MATCHING
        # ----------------------------------------------------

        st.subheader("💼 Role Matching")

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


        # ----------------------------------------------------
        # CREATE RESULTS TABLE
        # ----------------------------------------------------

        results_df = pd.DataFrame(results)


        # Sort by exact skill match
        results_df = results_df.sort_values(
            "Match Score (%)",
            ascending=False
        )


        # ----------------------------------------------------
        # RESULTS TABLE
        # ----------------------------------------------------

        st.dataframe(
            results_df,
            use_container_width=True
        )


        # ----------------------------------------------------
        # MATCH SCORE CHART
        # ----------------------------------------------------

        st.subheader("📊 Role Match Scores")

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


        # ----------------------------------------------------
        # BEST ROLE
        # ----------------------------------------------------

        best_role = results_df.iloc[0]

        st.success(
            f"🏆 Best Recommended Role: "
            f"{best_role['Role']} "
            f"({best_role['Match Score (%)']}% match)"
        )


        # ----------------------------------------------------
        # GET REQUIRED SKILLS
        # ----------------------------------------------------

        role_skills = roles[
            roles["role"] == best_role["Role"]
        ].iloc[0]["skills"]


        # ----------------------------------------------------
        # GENERATE EXPLANATION
        # ----------------------------------------------------

        matched_skills, missing_skills = get_explanation(
            skills,
            role_skills
        )


        # ----------------------------------------------------
        # EXPLANATION
        # ----------------------------------------------------

        st.subheader("🔍 Why this role was recommended")

        st.write("✅ Matched Skills")

        st.write(matched_skills)

        st.write("❌ Missing Skills")

        st.write(missing_skills)


        # ====================================================
        # FAIRNESS AUDIT
        # ====================================================

        st.divider()

        st.subheader("⚖️ Fairness Audit")

        st.caption(
            "Fairness evaluation using demonstration data "
            "for the academic project."
        )


        fairness_data = pd.read_csv(
            "data/fairness_eval.csv"
        )


        # ----------------------------------------------------
        # GROUP A SCORES
        # ----------------------------------------------------

        group_a_scores = fairness_data[
            fairness_data["Group"] == "Group_A"
        ]["Match_Score"].tolist()


        # ----------------------------------------------------
        # GROUP B SCORES
        # ----------------------------------------------------

        group_b_scores = fairness_data[
            fairness_data["Group"] == "Group_B"
        ]["Match_Score"].tolist()


        # ----------------------------------------------------
        # AVERAGE SCORES
        # ----------------------------------------------------

        average_a = sum(group_a_scores) / len(group_a_scores)

        average_b = sum(group_b_scores) / len(group_b_scores)


        # ----------------------------------------------------
        # FAIRNESS GAP
        # ----------------------------------------------------

        fairness_gap = abs(
            average_a - average_b
        )


        # ----------------------------------------------------
        # FAIRNESS RESULTS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Group A Average",
                f"{average_a:.2f}%"
            )


        with col2:

            st.metric(
                "Group B Average",
                f"{average_b:.2f}%"
            )


        with col3:

            st.metric(
                "Fairness Gap",
                f"{fairness_gap:.2f}%"
            )


        # ----------------------------------------------------
        # FAIRNESS INTERPRETATION
        # ----------------------------------------------------

        if fairness_gap <= 5:

            st.success(
                "✅ Low difference between the two groups."
            )

        elif fairness_gap <= 10:

            st.warning(
                "⚠️ Moderate difference between the two groups."
            )

        else:

            st.error(
                "🚨 High difference between the two groups."
            )


    else:

        st.warning(
            "No skills found in the resume."
        )