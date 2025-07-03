# Use Python 3.11 base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /workspace

# Create a non-root user and group
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser

# Install required OS packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies as root
COPY --chown=appuser:appgroup requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full project and change ownership
COPY --chown=appuser:appgroup . .

# Switch to the non-root user
USER appuser

# Expose Streamlit's default port
EXPOSE 8501

# Entry point
CMD ["streamlit", "run", "/workspace/src/app.py"]
