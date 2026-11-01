from dataclasses import dataclass

import streamlit as st


@dataclass
class WorkOutPlannerInput:
    fitnessGoal: str
    experienceLevel: str
    daysAvailableForWeek: int
    equipmentAccess: str
    injuries: str


# page layout
st.set_page_config(
    page_title="Workout Planner",
    layout="wide")

st.header("Workout Planner", text_alignment="center")


with st.form("User Workout Inputs", clear_on_submit=False):

    fitnessGoal, experienceLevel, daysAvailableForWeek, equipmentAccess, injuries = st.columns(5)
    with fitnessGoal:
        fitnessGoal_Input = st.selectbox(
            "Select Fitness Goal",
            options=["Build muscle", "Lose fat", "General fitness", "Improve endurance"],
            key="fitnessGoal_Input",

        )

    with experienceLevel:
        experienceLevel_Input = st.selectbox(
            "Select Experience Level",
            options=["Beginner", "Intermediate", "Advanced"],
            key="experienceLevel_Input"
        )

    with daysAvailableForWeek:
        daysAvailableForWeek_Input = st.slider(
            "Days Available For Week",
            min_value=1,
            max_value=7,
            key="daysAvailableForWeek_Input"
        )

    with equipmentAccess:
        equipmentAccess_Input = st.selectbox(
            "Equipment Access",
            options=["No equipment", "Home dumbbells", "Full Gym"],
            key="equipmentAccess_Input"
        )

    with injuries:
        injuries_Input = st.text_input(
            "Injuries Or Limitations",
            key="injuries_Input"
        )

submitted = st.button("Generate Plan", type="primary")



def call_llm(data: WorkOutPlannerInput) -> dict:
    """
    Captures the users input and invokes the LLM API

    :param data:
    :return: LLM API response
    """

    url = "";


if submitted:
    form_data = WorkOutPlannerInput(
        fitnessGoal= fitnessGoal_Input,
        experienceLevel= experienceLevel_Input,
        daysAvailableForWeek= daysAvailableForWeek_Input,
        equipmentAccess=equipmentAccess_Input,
        injuries= injuries_Input
    )

   # with st.spinner("Generating Plan..."):
   #    try:
   #        call_llm(form_data)
    #   except Exception as e:


# columns end

