import json
from google import genai
from google.genai import types
from typing import List, Dict, Any

from app.analyzer.json_to_object import JsonParser
from app.api.utils.config import Config
from google.genai.types import ThinkingConfig
from app.api.utils.llm_strings import get_system_instruction, create_security_analysis_prompt
from app.models.llm_result import Finding


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
    def parse_response(response_text: str) -> List[Finding]:
        json_to_findings = JsonParser(response_text)
        return json_to_findings.parse()


