import streamlit as st

from workout_planner.models.workout_input import WorkoutInput
from workout_planner.services.groq_client import GroqClient
from workout_planner.services.workout_planner_service import (
    WorkoutPlannerService
)


st.set_page_config(
    page_title="Workout Planner",
    layout="wide"
)

st.title("AI Workout Planner")


with st.form("workout_form"):

    col1, col2 = st.columns(2)

    with col1:
        fitness_goal = st.selectbox(
            "Fitness Goal",
            [
                "Build muscle",
                "Lose fat",
                "General fitness",
                "Improve endurance"
            ]
        )

        experience_level = st.selectbox(
            "Experience Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        days_per_week = st.slider(
            "Days Available Per Week",
            min_value=1,
            max_value=7,
            value=4
        )

    with col2:
        equipment_access = st.selectbox(
            "Equipment Access",
            ["No equipment", "Home dumbbells", "Full Gym"]
        )

        injuries = st.text_area(
            "Injuries or Physical Limitations",
            placeholder="Describe any limitations, or enter None"
        )

    submitted = st.form_submit_button(
        "Generate Plan",
        type="primary"
    )


if submitted:

    user_input = WorkoutInput(
        fitness_goal=fitness_goal,
        experience_level=experience_level,
        days_per_week=days_per_week,
        equipment_access=equipment_access,
        injuries=injuries
    )

    try:
        with st.spinner("Generating your workout plan..."):

            client = GroqClient()

            service = WorkoutPlannerService(client)

            workout_plan = service.generate_plan(user_input)

        st.subheader("Your Personalized Workout Plan")
        st.markdown(workout_plan)

    except Exception:
        st.error(
            "Unable to generate the workout plan. "
            "Please check the application logs."
        )