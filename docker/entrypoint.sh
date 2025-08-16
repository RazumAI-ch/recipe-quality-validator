#!/usr/bin/env sh
set -ex  # Exit on error, print each command

# Use Cloud Run PORT if available, otherwise fallback to 8080
PORT_TO_USE="${PORT:-8080}"

# Default bind address for Streamlit
ADDR_TO_USE="${STREAMLIT_SERVER_ADDRESS:-0.0.0.0}"

# Print context for debugging
echo "Container starting at $(date)"
echo "Running as user: $(whoami)"
echo "Expected port: $PORT_TO_USE"
echo "Bind address: $ADDR_TO_USE"
echo "App path: /workspace/src/app.py"

# Ensure Python dependencies are installed
echo "Installed Python packages:"
pip list

# Start Streamlit
exec streamlit run /workspace/src/app.py \
  --server.port="${PORT_TO_USE}" \
  --server.address="${ADDR_TO_USE}" \
  --server.headless=true
