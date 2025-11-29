from app.models.llm_result import Finding
from typing import Dict, Any, List
import structlog
import json

logger = structlog.get_logger(__name__)






class JsonParser:

    def __init__(self, json_string: str):
        self.json_string = json_string


    def _extract_json(self) -> str:
        """Extract JSON from markdown code blocks if present."""
        if "```json" in self.json_string:
            start = self.json_string.find("```json") + 7
            end = self.json_string.find("```", start)
            return self.json_string[start:end].strip()

        if "```" in self.json_string:
            start = self.json_string.find("```") + 3
            end = self.json_string.find("```", start)
            return self.json_string[start:end].strip()

        return self.json_string.strip()

    @staticmethod
    def _to_finding(item: Dict[str, Any]) -> Finding:

        return Finding(
            line=int(item.get("line", 0)),
            risk_score=int(item.get("risk_score", 0)),
            category=str(item.get("category", "Unknown")),
            description=str(item.get("description", "")),
            recommendation=str(item.get("recommendation", "")),
            raw_output=item.get("raw_output")
        )


    def parse(self) -> List[Finding]:

        try:
            json_data = self._extract_json()
            loaded_json = json.loads(json_data)

            return [self._to_finding(item) for item in loaded_json]

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f"⚠️ Could not parse LLM response as JSON: {e}")
            return [Finding(
                line=0,
                risk_score=5,
                category="Analysis Error",
                description="Could not parse structured response",
                recommendation="Review raw LLM output",
                raw_output=self.json_string
            )]
