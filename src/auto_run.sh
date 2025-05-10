#!/bin/bash

# Exit on error
set -e

# Start FastAPI (edit the path/module as needed)
# Example: uvicorn main:app --reload --port 9090
python src/main.py

# Wait for the API to be up (adjust if needed)
echo "Waiting for FastAPI to start..."
sleep 5

# Start Streamlit app (edit the path as needed)
streamlit run src/comms/client/streamlit/app.py

# When Streamlit exits, kill the FastAPI server
echo "Stopping FastAPI (PID $API_PID)..."
kill $API_PID
