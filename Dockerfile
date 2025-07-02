# Use Python 3.11 base image
FROM python:3.11-slim

# Set the working directory (compose overrides to /workspace)
WORKDIR /workspace

# Install required OS packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full project
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Entry point (overridden by docker-compose)
CMD ["streamlit", "run", "src/app.py"]