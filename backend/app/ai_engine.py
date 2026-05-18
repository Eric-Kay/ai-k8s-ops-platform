from typing import Dict, List


def analyse_with_ai(logs: str, events: str) -> Dict:
    combined_text = f"{logs}\n{events}".lower()

    causes: List[str] = []
    actions: List[str] = []
    severity = "low"

    if "crashloopbackoff" in combined_text:
        causes.append("The pod is repeatedly crashing after startup.")
        actions.append("Check application startup command, environment variables, secrets, and dependencies.")
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
        "issue_summary": "AI-assisted Kubernetes incident analysis completed.",
        "possible_causes": causes,
        "recommended_actions": actions,
        "severity": severity,
    }