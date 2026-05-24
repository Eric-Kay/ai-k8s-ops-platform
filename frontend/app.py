import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Kubernetes Operations Platform",
    layout="wide"
)

st.title("AI Kubernetes Operations Platform")
st.write("AI-assisted Kubernetes troubleshooting with PostgreSQL incident history.")

namespace = st.text_input("Kubernetes Namespace", value="ai-k8s-ops")
pod_name = st.text_input("Pod Name (optional)")

st.subheader("Manual Logs and Events")

logs = st.text_area(
    "Paste pod logs here",
    height=200
)

events = st.text_area(
    "Paste Kubernetes events here",
    height=150
)

if st.button("Analyse Issue"):

    payload = {
        "namespace": namespace,
        "pod_name": pod_name if pod_name else None,
        "logs": logs if logs else None,
        "events": events if events else None
    }

    with st.spinner("Analysing Kubernetes incident..."):

        try:
            response = requests.post(
                f"{BACKEND_URL}/troubleshoot",
                json=payload,
                timeout=180
            )

            response.raise_for_status()

            data = response.json()

            st.success(data["issue_summary"])

            severity = data.get("severity", "unknown").upper()

            if severity == "CRITICAL":
                st.error(f"Severity: {severity}")
            elif severity == "HIGH":
                st.warning(f"Severity: {severity}")
            else:
                st.info(f"Severity: {severity}")

            st.subheader("Possible Causes")

            for cause in data.get("possible_causes", []):
                st.markdown(f"- {cause}")

            st.subheader("Recommended Actions")

            for action in data.get("recommended_actions", []):
                st.markdown(f"- {action}")

        except requests.exceptions.Timeout:
            st.error(
                "Backend analysis timed out after 180 seconds. "
                "Check backend logs and OpenAI connectivity."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to backend service. "
                "Verify the backend deployment and service are running."
            )

        except requests.exceptions.HTTPError:
            st.error("Backend returned an error.")
            st.code(response.text)

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

st.divider()

st.subheader("Incident History")

if st.button("Load Incident History"):

    try:
        response = requests.get(
            f"{BACKEND_URL}/history",
            timeout=30
        )

        response.raise_for_status()

        history = response.json()

        if history:
            st.dataframe(history, use_container_width=True)
        else:
            st.info("No incident history found.")

    except Exception as e:
        st.error(f"Failed to load history: {str(e)}")

st.divider()

st.subheader("List Pods")

if st.button("Fetch Pods"):

    try:
        response = requests.get(
            f"{BACKEND_URL}/pods/{namespace}",
            timeout=30
        )

        response.raise_for_status()

        st.json(response.json())

    except Exception as e:
        st.error(f"Failed to fetch pods: {str(e)}")