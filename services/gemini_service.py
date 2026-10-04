import json
import re

from typing import Any, Optional

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

from services.mock_recommendations import (
    home_mock,
    party_mock,
    jewelry_mock,
)


try:

    from google import genai

    from google.genai import types

except Exception:

    genai = None

    types = None


class GeminiService:

    def __init__(self):

        self.enabled = bool(
            GEMINI_API_KEY
            and genai
        )

        self.client = (
            genai.Client(
                api_key=GEMINI_API_KEY
            )
            if self.enabled
            else None
        )


    def _extract_json(
        self,
        text: str,
    ) -> dict:

        text = (text or "").strip()

        if text.startswith("```"):

            text = re.sub(
                r"^```(?:json)?\s*",
                "",
                text,
            )

            text = re.sub(
                r"\s*```$",
                "",
                text,
            )

        try:

            return json.loads(text)

        except json.JSONDecodeError:

            match = re.search(
                r"\{.*\}",
                text,
                re.S,
            )

            if match:

                return json.loads(
                    match.group(0)
                )

            raise


    def _build_prompt(
        self,
        planner_type: str,
        data: dict,
    ) -> str:

        return f"""
You are PocketSmart AI,
a budget-aware recommendation assistant.

Planner:
{planner_type}

User data:

{json.dumps(
    data,
    ensure_ascii=False,
    indent=2
)}

Return ONLY valid JSON.

Do not use markdown.

Use exactly this structure:

{{
    "summary": "short explanation",

    "budget_allocation": [
        {{
            "category": "string",
            "amount": 0,
            "percentage": 0
        }}
    ],

    "recommendations": [
        {{
            "title": "string",
            "estimated_price": 0,
            "platform": "Amazon|Flipkart|IKEA|Swiggy|Zomato|OYO|Other",
            "description": "string",
            "search_url": "string",
            "reason": "string"
        }}
    ],

    "savings_tips": [
        "string"
    ]
}}

Rules:

1. Stay within the stated budget.

2. Provide 4 to 6 recommendations.

3. Never claim live stock.

4. Never claim a live price unless it was explicitly supplied.

5. Search URLs are discovery links.

6. Consider the user's style and requirements.

7. For jewelry, consider occasion, style and outfit description.

8. If an image is attached, use it as a visual reference.

9. Keep explanations concise.

10. Return valid JSON only.
"""


    def generate(
        self,
        planner_type: str,
        data: dict,
        image_bytes: Optional[bytes] = None,
        mime_type: Optional[str] = None,
    ) -> dict:

        if not self.enabled:

            return self._mock(
                planner_type,
                data,
            )

        contents: Any = [
            self._build_prompt(
                planner_type,
                data,
            )
        ]

        if (
            image_bytes
            and mime_type
            and types
        ):

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                )
            )

        try:

            response = (
                self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=0.4,
                        response_mime_type="application/json",
                    ),
                )
            )

            result = self._extract_json(
                response.text
            )

            return self._normalize(
                result,
                planner_type,
                data,
            )

        except Exception:

            return self._mock(
                planner_type,
                data,
            )


    def _normalize(
        self,
        result: dict,
        planner_type: str,
        data: dict,
    ) -> dict:

        result.setdefault(
            "summary",
            "AI-generated recommendation plan.",
        )

        result.setdefault(
            "budget_allocation",
            [],
        )

        result.setdefault(
            "recommendations",
            [],
        )

        result.setdefault(
            "savings_tips",
            [],
        )

        if not result["recommendations"]:

            return self._mock(
                planner_type,
                data,
            )

        for recommendation in result[
            "recommendations"
        ]:

            recommendation.setdefault(
                "platform",
                "Other",
            )

            recommendation.setdefault(
                "estimated_price",
                0,
            )

            recommendation.setdefault(
                "description",
                "",
            )

            recommendation.setdefault(
                "reason",
                "",
            )

            recommendation.setdefault(
                "search_url",
                "",
            )

        return result


    def _mock(
        self,
        planner_type,
        data,
    ):

        if planner_type == "home":

            return home_mock(data)

        if planner_type == "party":

            return party_mock(data)

        return jewelry_mock(data)


gemini_service = GeminiService()