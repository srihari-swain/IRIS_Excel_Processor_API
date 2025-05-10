import streamlit as st
import requests

st.title("API Tester ")

# Set your API base URL
API_URL = st.text_input("API base URL", "http://localhost:9090")

# List your endpoints and their parameters here
endpoints = {
    "list_tables": {
        "method": "GET",
        "path": "/list_tables",
        "params": []
    },
    "get_table_details": {
        "method": "GET",
        "path": "/get_table_details",
        "params": ["table_name"]
    },
    "row_sum": {
        "method": "GET",
        "path": "/row_sum",
        "params": ["table_name", "row_name"]
    },
    "row_min": {
        "method": "GET",
        "path": "/row_min",
        "params": ["table_name", "row_name"]
    },
    "row_max": {
        "method": "GET",
        "path": "/row_max",
        "params": ["table_name", "row_name"]
    },
}

endpoint_name = st.selectbox("Select endpoint", list(endpoints.keys()))
endpoint = endpoints[endpoint_name]

# Dynamically create input fields for parameters, if any
params = {}
if endpoint["params"]:
    for param in endpoint["params"]:
        params[param] = st.text_input(f"{param}")

if st.button("Send Request"):
    url = API_URL.rstrip("/") + endpoint["path"]
    try:
        if endpoint["method"] == "GET":
            resp = requests.get(url, params=params if params else None)
        else:
            resp = requests.post(url, json=params if params else None)
        st.code(f"Status code: {resp.status_code}", language="python")
        try:
            st.json(resp.json())
        except Exception:
            st.write(resp.text)
    except Exception as e:
        st.error(str(e))
