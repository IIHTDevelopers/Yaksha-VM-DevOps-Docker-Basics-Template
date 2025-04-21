FROM python:3.9-slim

WORKDIR /app

# Add a label to identify this as a yaksha container
LABEL name="yaksha-test-container"

# Copy requirements (if any)
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Command to keep container running for testing
CMD ["python", "-c", "import time; print('Yaksha container is running...'); time.sleep(3600)"]
