# Use Python 3.11 base image
FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r appgroup && useradd --no-log-init -r -m -g appgroup appuser

# Install required OS packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install needed certificates
WORKDIR /etc/ssl/certs/
RUN curl -O https://certinfo.roche.com/rootcerts/Roche%20G3%20Root%20CA.crt
RUN curl --remote-name-all "https://certinfo.roche.com/rootcerts/Roche%20G3%20Issuing%20CA%20[1-6].crt"

# Set the working directory
WORKDIR /workspace

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
