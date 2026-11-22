import json
import urllib.request
import urllib.error

from workout_planner.config import GROQ_API_KEY
from workout_planner.models.llm_request import LLMRequest


class GroqClient:

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, api_key: str | None = None):
        self._api_key = api_key or GROQ_API_KEY

        if not self._api_key:
            raise ValueError("GROQ_API_KEY is not configured")

    def generate(self, request: LLMRequest) -> str:

        body = json.dumps(request.to_dict()).encode("utf-8")

        http_request = urllib.request.Request(
            url=self.BASE_URL,
            data=body,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "User-Agent": "WorkoutPlannerApp/1.0"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(
                http_request, timeout=60
            ) as response:

                result = json.load(response)

                return result["choices"][0]["message"]["content"]

        except urllib.error.HTTPError as error:
            error_body = error.read().decode("utf-8")
            raise RuntimeError(
                f"Groq HTTP {error.code}: {error_body}"
            ) from error

        except urllib.error.URLError as error:
            raise RuntimeError(
                f"Groq connection failed: {error.reason}"
            ) from error