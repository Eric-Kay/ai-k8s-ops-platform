import json
import os
from typing import Dict, List

from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def fallback_analysis(logs: str, events: str) -> Dict:
    combined_text = f"{logs}\n{events}".lower()

    causes: List[str] = []
    actions: List[str] = []
    severity = "low"

    if "crashloopbackoff" in combined_text:
        causes.append("The pod is repeatedly crashing after startup.")
        actions.append("Check startup command, environment variables, secrets, and dependencies.")
        severity = "high"

    if "oomkilled" in combined_text:
        causes.append("The container exceeded its memory limit and was killed.")
        actions.append("Increase memory limits or optimise application memory usage.")
        severity = "high"

    if "imagepullbackoff" in combined_text:
        causes.append("Kubernetes cannot pull the container image.")
        actions.append("Verify image name, tag, registry credentials, and imagePullSecrets.")
        severity = "medium"

    if "failed scheduling" in combined_text:
        causes.append("The pod cannot be scheduled on available nodes.")
        actions.append("Check node capacity, taints, tolerations, affinity rules, and resource requests.")
        severity = "medium"

    if "connection refused" in combined_text:
        causes.append("The application may be trying to reach a service that is unavailable.")
        actions.append("Verify service DNS, ports, readiness probes, and backend dependencies.")
        severity = "medium"

    if not causes:
        causes.append("No known Kubernetes failure pattern detected.")
        actions.append("Review pod logs, events, resource limits, probes, service configuration, and deployment history.")

    return {
        "issue_summary": "Rule-based Kubernetes incident analysis completed.",
        "possible_causes": causes,
        "recommended_actions": actions,
        "severity": severity,
    }


def analyse_with_ai(logs: str, events: str) -> Dict:
    if not os.getenv("OPENAI_API_KEY"):
        return fallback_analysis(logs, events)

    prompt = f"""
You are a senior Kubernetes SRE and Cloud Platform Engineer.

Analyze the Kubernetes pod logs and events below.

Return ONLY valid JSON with this exact structure:
{{
  "issue_summary": "short summary",
  "possible_causes": ["cause 1", "cause 2"],
  "recommended_actions": ["action 1", "action 2"],
  "severity": "low|medium|high|critical"
}}

Pod logs:
{logs}

Kubernetes events:
{events}
"""

    try:
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5.5"),
            input=prompt,
        )

        raw_output = response.output_text.strip()
        parsed = json.loads(raw_output)

        return {
            "issue_summary": parsed.get("issue_summary", "AI Kubernetes incident analysis completed."),
            "possible_causes": parsed.get("possible_causes", []),
            "recommended_actions": parsed.get("recommended_actions", []),
            "severity": parsed.get("severity", "medium"),
        }

    except Exception as error:
        fallback = fallback_analysis(logs, events)
        fallback["issue_summary"] = f"OpenAI analysis failed, fallback analysis used. Error: {str(error)}"
        return fallback