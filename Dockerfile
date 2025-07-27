# Use an AMD64-compatible lightweight base image
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory in container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script
COPY extract_structure.py .

# Create input/output dirs
RUN mkdir input output

# Set default command to run the script
CMD ["python", "extract_structure.py"]
