
import unittest

from workout_planner.models.workout_input import WorkoutInput
from workout_planner.models.llm_request import LLMMessage, LLMRequest


class TestWorkoutInput(unittest.TestCase):

    def test_create_workout_input(self):
        workout = WorkoutInput(
            fitness_goal="Build muscle",
            experience_level="Beginner",
            days_per_week=3,
            equipment_access="Full Gym",
            injuries="None"
        )

        self.assertEqual(workout.fitness_goal, "Build muscle")
        self.assertEqual(workout.days_per_week, 3)
        self.assertEqual(workout.injuries, "None")


class TestLLMRequest(unittest.TestCase):

    def test_request_serialization(self):
        request = LLMRequest(
            model="openai/gpt-oss-120b",
            messages=[
                LLMMessage(role="system", content="You are a coach"),
                LLMMessage(role="user", content="Build muscle")
            ]
        )

        result = request.to_dict()

        self.assertEqual(result["model"], "openai/gpt-oss-120b")
        self.assertEqual(result["temperature"], 0.4)
        self.assertEqual(len(result["messages"]), 2)
        self.assertEqual(result["messages"][0]["role"], "system")
        self.assertEqual(result["messages"][1]["content"], "Build muscle")

    def test_empty_message_list(self):
        request = LLMRequest(model="test-model", messages=[])

        self.assertEqual(request.to_dict()["messages"], [])


if __name__ == "__main__":
    unittest.main()
