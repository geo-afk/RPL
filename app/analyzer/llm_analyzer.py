import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from app.api.utils.config import Config
from google.genai.types import ThinkingConfig
from app.api.utils.llm_strings import get_system_instruction, create_security_analysis_prompt

load_dotenv()


from google import genai
from google.genai import types


class LLMAnalyzer:

    def __init__(self):
        self.client = genai.Client(
            api_key = Config().get("GEMINI_API_KEY")
        )

        self.model = "gemini-2.5-flash"


    def security_policy_analysis(self, rpl_code: str):

        security_prompt = create_security_analysis_prompt(rpl_code)

        content = self.get_policy(security_prompt)
        config = self.get_content_config()

        response = self.generate(content, config)

        findings = self.parse_response(response)

        return findings


    @staticmethod
    def get_policy(prompt: str):

        content = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=prompt,
                    )
                ]
            )
        ]

        return content


    @staticmethod
    def get_content_config():
        generate_content_config = types.GenerateContentConfig(
            thinking_config=ThinkingConfig(thinking_budget=-1),
            system_instruction=[
                types.Part.from_text(
                    text=get_system_instruction()
                )
            ],
        )


        return generate_content_config


    def generate(self, contents: List[types.Content], config: types.GenerateContentConfig) -> str:

        response = ""

        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=config
        ):

            response += chunk.text


        return response

    @staticmethod
    def parse_response(response_text: str) -> List[Dict[str, Any]]:
        """Parse LLM response into structured findings."""
        try:
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                json_text = response_text[start:end].strip()
            else:
                json_text = response_text
            findings = json.loads(json_text)
            return findings
        except json.JSONDecodeError:
            print("⚠️ Could not parse LLM response as JSON")
            return [{
                'line': 0,
                'risk_score': 5,
                'category': 'Analysis Error',
                'description': 'Could not parse structured response',
                'recommendation': 'Review raw LLM output',
                'raw_output': response_text
            }]

