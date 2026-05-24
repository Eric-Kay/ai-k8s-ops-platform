import json
import os
from typing import Dict, List

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30.0,
)


def fallback_analysis(logs: str, events: str) -> Dict:
    return {
        "issue_summary": "Fallback Kubernetes incident analysis completed.",
        "possible_causes": [
            "Backend service may be unable to reach PostgreSQL.",
            "Readiness probe is failing because the application is not responding in time.",
            "The pod may be restarting due to dependency or startup failure."
        ],
        "recommended_actions": [
            "Verify RDS endpoint, security groups, and database credentials.",
            "Check backend pod logs for database connection errors.",
            "Confirm Kubernetes secrets are correctly mounted.",
            "Review readiness and liveness probe timing."
        ],
        "severity": "medium",
    }


def analyse_with_ai(logs: str, events: str) -> Dict:
    if not os.getenv("OPENAI_API_KEY"):
        return fallback_analysis(logs, events)

    prompt = f"""
You are a senior Kubernetes SRE.

Analyze these Kubernetes logs and events.

Return ONLY valid JSON with this structure:
{{
  "issue_summary": "short summary",
  "possible_causes": ["cause 1", "cause 2"],
  "recommended_actions": ["action 1", "action 2"],
  "severity": "low|medium|high|critical"
}}

Logs:
{logs}

Events:
{events}
"""

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            input=prompt,
        )

        data = json.loads(response.output_text)

        return {
            "issue_summary": data.get("issue_summary", "AI Kubernetes incident analysis completed."),
            "possible_causes": data.get("possible_causes", []),
            "recommended_actions": data.get("recommended_actions", []),
            "severity": data.get("severity", "medium"),
        }

    except Exception:
        return fallback_analysis(logs, events)