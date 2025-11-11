import os
from openai import OpenAI
from dotenv import load_dotenv
import json


load_dotenv()


class LLMSecurityAnalyzer:
    """
    Uses LLM to analyze security policies for potential risks.
    """

    def __init__(self, model="gpt-4o-mini"):
        """Initialize with OpenAI API key from environment."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment. "
                "Please set it in your .env file"
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def analyze_policies(self, policies, roles, resources):
        """
        Analyze policies for security risks using LLM.

        Returns:
            List of findings with risk scores and explanations
        """
        # Prepare policy context
        policy_text = self._format_policies_for_llm(policies, roles, resources)

        # Create prompt for LLM
        prompt = self._create_security_analysis_prompt(policy_text)

        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a security expert analyzing access control "
                            "policies. Identify potential security risks, "
                            "overly permissive rules, logical contradictions, "
                            "and violations of least privilege principle."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent analysis
                max_tokens=2000
            )

            # Extract and parse response
            analysis = response.choices[0].message.content
            findings = self._parse_llm_response(analysis)

            return findings

        except Exception as e:
            print(f"❌ LLM Analysis Error: {str(e)}")
            return []

    def _format_policies_for_llm(self, policies, roles, resources):
        """Format policies in a readable way for LLM."""
        output = "=== ACCESS CONTROL POLICIES ===\n\n"

        # Add roles
        output += "ROLES:\n"
        for role_name, permissions in roles.items():
            output += f"  - {role_name}: {', '.join(permissions)}\n"
        output += "\n"

        # Add resources
        output += "RESOURCES:\n"
        for resource_name, attrs in resources.items():
            output += f"  - {resource_name}\n"
        output += "\n"

        # Add policies
        output += "POLICIES:\n"
        for i, policy in enumerate(policies, 1):
            output += f"  {i}. {policy['type']} "
            output += f"actions: {', '.join(policy['actions'])} "
            output += f"ON resource: {policy['resource']}"
            if policy.get('condition'):
                output += f" IF {policy['condition']}"
            output += f" (Line {policy['line']})\n"

        return output

    def _create_security_analysis_prompt(self, policy_text):
        """Create detailed prompt for security analysis."""
        return f"""
        Analyze the following access control policies for security risks:

        {policy_text}

        Please identify:
        1. **Overly Permissive Policies**: Rules that grant excessive access (e.g., wildcards, broad permissions)
        2. **Privilege Escalation Risks**: Scenarios where users could gain unauthorized elevated access
        3. **Logical Contradictions**: Conflicting ALLOW/DENY rules
        4. **Least Privilege Violations**: Cases where access exceeds what's necessary
        5. **Missing Restrictions**: Resources or actions without proper controls
        6. **Temporal Vulnerabilities**: Time-based conditions that could be exploited

        For each issue found, provide:
        - **Line number** (if applicable)
        - **Risk score** (1-10, where 10 is critical)
        - **Description** of the security concern
        - **Recommendation** for mitigation

        Format your response as JSON array:
        [
          {{
            "line": <line_number>,
            "risk_score": <1-10>,
            "category": "<category>",
            "description": "<description>",
            "recommendation": "<recommendation>"
          }}
        ]
        """

    def _parse_llm_response(self, response_text):
        """Parse LLM response into structured findings."""
        try:
            # Try to extract JSON from response
            # LLM might wrap JSON in markdown code blocks
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
            # Fallback: return raw text as single finding
            print("⚠️  Could not parse LLM response as JSON")
            return [{
                'line': 0,
                'risk_score': 5,
                'category': 'Analysis Error',
                'description': 'Could not parse structured response',
                'recommendation': 'Review raw LLM output',
                'raw_output': response_text
            }]

    def print_findings(self, findings):
        """Print formatted security findings."""
        if not findings:
            print("\n✓ No security issues identified by LLM")
            return

        print(f"\n🔍 LLM Security Analysis Found {len(findings)} Issue(s):\n")

        # Sort by risk score (highest first)
        sorted_findings = sorted(
            findings,
            key=lambda x: x.get('risk_score', 0),
            reverse=True
        )

        for i, finding in enumerate(sorted_findings, 1):
            risk = finding.get('risk_score', 0)
            risk_emoji = "🔴" if risk >= 8 else "🟡" if risk >= 5 else "🟢"

            print(f"{i}. {risk_emoji} Risk Score: {risk}/10")
            if finding.get('line'):
                print(f"   Line: {finding['line']}")
            print(f"   Category: {finding.get('category', 'Unknown')}")
            print(f"   Issue: {finding.get('description', 'No description')}")
            print(f"   Recommendation: {finding.get('recommendation', 'No recommendation')}")
            print()

# Alternative: Azure OpenAI
class AzureOpenAIAnalyzer(LLMSecurityAnalyzer):
    """Use Azure OpenAI Service instead of OpenAI API."""

    def __init__(self, deployment_name="gpt-4"):
        from openai import AzureOpenAI

        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.model = deployment_name