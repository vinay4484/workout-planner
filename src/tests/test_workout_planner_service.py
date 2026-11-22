
import json
import unittest
from unittest.mock import Mock

from workout_planner.models.workout_input import WorkoutInput
from workout_planner.services.workout_planner_service import (
    WorkoutPlannerService
)


class TestWorkoutPlannerService(unittest.TestCase):

    def setUp(self):
        self.mock_client = Mock()
        self.mock_client.generate.return_value = "# Your Workout Plan"

        self.service = WorkoutPlannerService(self.mock_client)

        self.user_input = WorkoutInput(
            fitness_goal="Build muscle",
            experience_level="Intermediate",
            days_per_week=4,
            equipment_access="Full Gym",
            injuries="Knee discomfort"
        )

    def test_generate_plan_returns_llm_response(self):
        result = self.service.generate_plan(self.user_input)

        self.assertEqual(result, "# Your Workout Plan")
        self.mock_client.generate.assert_called_once()

    def test_generate_plan_sends_correct_model(self):
        self.service.generate_plan(self.user_input)

        request = self.mock_client.generate.call_args.args[0]

        self.assertEqual(request.model, "openai/gpt-oss-120b")
        self.assertEqual(request.temperature, 0.4)

    def test_generate_plan_includes_system_prompt(self):
        self.service.generate_plan(self.user_input)

        request = self.mock_client.generate.call_args.args[0]

        self.assertEqual(request.messages[0].role, "system")
        self.assertIn("12-week fitness plan", request.messages[0].content)

    def test_generate_plan_includes_user_context(self):
        self.service.generate_plan(self.user_input)

        request = self.mock_client.generate.call_args.args[0]
        user_context = json.loads(request.messages[1].content)

        self.assertEqual(request.messages[1].role, "user")
        self.assertEqual(user_context["fitness_goal"], "Build muscle")
        self.assertEqual(user_context["days_per_week"], 4)
        self.assertEqual(user_context["injuries"], "Knee discomfort")

    def test_generate_plan_propagates_client_error(self):
        self.mock_client.generate.side_effect = RuntimeError(
            "Groq service unavailable"
        )

        with self.assertRaisesRegex(
            RuntimeError, "Groq service unavailable"
        ):
            self.service.generate_plan(self.user_input)


if __name__ == "__main__":
    unittest.main()
