from kubernetes import client, config
from kubernetes.client.rest import ApiException


def load_kube_config():
    try:
        config.load_incluster_config()
    except Exception:
        config.load_kube_config()


def get_pod_logs(namespace: str, pod_name: str) -> str:
    load_kube_config()
    v1 = client.CoreV1Api()

    try:
        return v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            tail_lines=100
        )
    except ApiException as error:
        return f"Error reading pod logs: {error}"


def get_namespace_events(namespace: str) -> str:
    load_kube_config()
    v1 = client.CoreV1Api()

    try:
        events = v1.list_namespaced_event(namespace=namespace)
        return "\n".join(
            f"{event.type} | {event.reason} | {event.message}"
            for event in events.items
        )
    except ApiException as error:
        return f"Error reading Kubernetes events: {error}"


def list_pods(namespace: str):
    load_kube_config()
    v1 = client.CoreV1Api()

    try:
        pods = v1.list_namespaced_pod(namespace=namespace)
        return [
            {
                "name": pod.metadata.name,
                "phase": pod.status.phase,
                "node": pod.spec.node_name,
            }
            for pod in pods.items
        ]
    except ApiException as error:
        return [{"error": str(error)}]