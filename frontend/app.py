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

namespace = st.text_input("Kubernetes Namespace", value="default")
pod_name = st.text_input("Pod Name optional")

st.subheader("Manual Logs and Events")

logs = st.text_area("Paste pod logs here", height=200)
events = st.text_area("Paste Kubernetes events here", height=150)

if st.button("Analyse Issue"):
    payload = {
        "namespace": namespace,
        "pod_name": pod_name if pod_name else None,
        "logs": logs if logs else None,
        "events": events if events else None
    }

    response = requests.post(
        f"{BACKEND_URL}/troubleshoot",
        json=payload,
        timeout=60
    )

    if response.status_code == 200:
        data = response.json()

        st.success(data["issue_summary"])
        st.metric("Severity", data["severity"].upper())

        st.subheader("Possible Causes")
        for cause in data["possible_causes"]:
            st.write(f"- {cause}")

        st.subheader("Recommended Actions")
        for action in data["recommended_actions"]:
            st.write(f"- {action}")
    else:
        st.error("Failed to analyse issue")
        st.write(response.text)

st.divider()

st.subheader("Incident History")

if st.button("Load Incident History"):
    response = requests.get(f"{BACKEND_URL}/history", timeout=30)

    if response.status_code == 200:
        st.dataframe(response.json())
    else:
        st.error("Failed to load history")

st.divider()

st.subheader("List Pods")

if st.button("Fetch Pods"):
    response = requests.get(f"{BACKEND_URL}/pods/{namespace}", timeout=30)

    if response.status_code == 200:
        st.json(response.json())
    else:
        st.error("Failed to fetch pods")