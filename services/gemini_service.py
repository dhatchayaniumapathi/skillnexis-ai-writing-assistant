
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.5-flash-lite"


class GeminiService:

    def __init__(self):

        if not API_KEY:
            raise ValueError("Gemini API key is missing.")

        self.client = genai.Client(api_key=API_KEY)

    def generate_content(self, prompt, temperature=0.7):

        start_time = time.perf_counter()

        try:

            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "temperature": temperature
                }
            )

            content = response.text

            if not content:
                raise ValueError("Gemini returned an empty response.")

            latency = round(
                time.perf_counter() - start_time, 2
            )

            return {
                "content": content,
                "latency": latency,
                "model": MODEL_NAME,
                "status": "success"
            }

        except errors.APIError as error:

            raise RuntimeError(
                f"Gemini API error: {error}"
            ) from error
