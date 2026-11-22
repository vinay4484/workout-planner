
import io
import json
import unittest
import urllib.error
from unittest.mock import Mock, patch

from workout_planner.models.llm_request import LLMMessage, LLMRequest
from workout_planner.services.groq_client import GroqClient


class TestGroqClient(unittest.TestCase):

    def setUp(self):
        self.client = GroqClient(api_key="test-api-key")

        self.request = LLMRequest(
            model="openai/gpt-oss-120b",
            messages=[
                LLMMessage(role="user", content="Build muscle")
            ]
        )

    @patch("urllib.request.urlopen")
    def test_generate_success(self, mock_urlopen):
        api_response = {
            "choices": [
                {
                    "message": {
                        "content": "# Your Workout Plan"
                    }
                }
            ]
        }

        mock_response = Mock()
        mock_response.read.return_value = json.dumps(
            api_response
        ).encode("utf-8")

        mock_urlopen.return_value.__enter__.return_value = (
            mock_response
        )

        result = self.client.generate(self.request)

        self.assertEqual(result, "# Your Workout Plan")
        mock_urlopen.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_http_request_properties(self, mock_urlopen):
        mock_response = Mock()
        mock_response.read.return_value = (
            b'{"choices":[{"message":{"content":"OK"}}]}'
        )
        mock_urlopen.return_value.__enter__.return_value = (
            mock_response
        )

        self.client.generate(self.request)

        http_request = mock_urlopen.call_args.args[0]

        self.assertEqual(
            http_request.full_url,
            "https://api.groq.com/openai/v1/chat/completions"
        )
        self.assertEqual(http_request.get_method(), "POST")
        self.assertEqual(
            http_request.get_header("Authorization"),
            "Bearer test-api-key"
        )

        payload = json.loads(http_request.data.decode("utf-8"))

        self.assertEqual(payload["model"], "openai/gpt-oss-120b")
        self.assertEqual(payload["messages"][0]["role"], "user")
        self.assertEqual(payload["messages"][0]["content"], "Build muscle")

    @patch("urllib.request.urlopen")
    def test_http_error(self, mock_urlopen):
        error = urllib.error.HTTPError(
            url=GroqClient.BASE_URL,
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=io.BytesIO(b'{"error":"Invalid API key"}')
        )

        mock_urlopen.side_effect = error

        with self.assertRaisesRegex(RuntimeError, "HTTP 401"):
            self.client.generate(self.request)

    @patch("urllib.request.urlopen")
    def test_network_error(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError(
            "Connection refused"
        )

        with self.assertRaisesRegex(
            RuntimeError, "Connection refused"
        ):
            self.client.generate(self.request)

    @patch(
        "workout_planner.services.groq_client.GROQ_API_KEY",
        None
    )
    def test_missing_api_key(self):
        with self.assertRaisesRegex(
            ValueError, "GROQ_API_KEY is not configured"
        ):
            GroqClient(api_key=None)


if __name__ == "__main__":
    unittest.main()
