# File: Dockerfile
# Use Python 3.11 base image
FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r appgroup && useradd --no-log-init -r -m -g appgroup appuser

# Install required OS packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Roche certificates
WORKDIR /etc/ssl/certs/
RUN curl -O https://certinfo.roche.com/rootcerts/Roche%20G3%20Root%20CA.crt && \
    curl --remote-name-all "https://certinfo.roche.com/rootcerts/Roche%20G3%20Issuing%20CA%20[1-6].crt"

# Set working directory for app
WORKDIR /workspace

# Copy entrypoint first and make it executable
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy the rest of the app with ownership to non-root user
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Expose default Streamlit port
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
