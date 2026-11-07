
import json

from services.gemini_service import GeminiService


class EvaluationService:

    def __init__(self):
        self.gemini = GeminiService()

    def evaluate_content(self, user_request, generated_content):

        evaluation_prompt = f"""
        You are an AI content quality evaluator.

        Evaluate the generated content based on the
        user's original request.

        USER REQUEST:
        {user_request}

        GENERATED CONTENT:
        {generated_content}

        Evaluate these four dimensions:

        1. Relevance
        2. Clarity
        3. Completeness
        4. Instruction Following

        Give each dimension a score from 1 to 10.

        Return ONLY valid JSON in this format:

        {{
            "relevance": 8,
            "clarity": 9,
            "completeness": 8,
            "instruction_following": 9,
            "overall_score": 8.5,
            "strengths": [
                "Clear explanation",
                "Relevant examples"
            ],
            "improvements": [
                "Add more supporting details",
                "Improve the conclusion"
            ],
            "feedback": "The content is well structured."
        }}
        """

        result = self.gemini.generate_content(
            prompt=evaluation_prompt,
            temperature=0.2
        )

        raw_response = result["content"]

        try:
            evaluation = json.loads(raw_response)

        except json.JSONDecodeError as error:
            raise ValueError(
                "The evaluation response was not valid JSON."
            ) from error

        score_fields = [
            "relevance",
            "clarity",
            "completeness",
            "instruction_following"
        ]

        for field in score_fields:

            score = evaluation.get(field)

            if (
                isinstance(score, bool)
                or not isinstance(score, (int, float))
                or not 1 <= score <= 10
            ):
                raise ValueError(
                    f"Invalid evaluation score: {field}"
                )

        overall = evaluation.get("overall_score")

        if (
            isinstance(overall, bool)
            or not isinstance(overall, (int, float))
            or not 1 <= overall <= 10
        ):
            raise ValueError("Invalid overall score.")

        for field in ["strengths", "improvements"]:

            if (
                not isinstance(evaluation.get(field), list)
                or not all(
                    isinstance(item, str)
                    for item in evaluation[field]
                )
            ):
                raise ValueError(
                    f"Invalid evaluation field: {field}"
                )

        if not isinstance(evaluation.get("feedback"), str):
            raise ValueError("Invalid evaluation feedback.")

        return evaluation
