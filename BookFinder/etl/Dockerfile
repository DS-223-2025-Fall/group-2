FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app 

# ➡️ CHANGE 1: Set the primary Python path in the image ⬅️
ENV PYTHONPATH=/app

# Copy requirements file and install dependencies
COPY requirements.txt . 
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the rest of the application code
# ➡️ CHANGE 2: Copy code into the new WORKDIR (/app) ⬅️
COPY . /app/ 

# Create a non-root user and switch to it for security and stability
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Expose port 3000
EXPOSE 3000

# ➡️ CHANGE 3: Use the robust Uvicorn command ⬅️
CMD ["uvicorn", "etl_process:app", "--app-dir", "/app", "--host", "0.0.0.0", "--port", "3000"]