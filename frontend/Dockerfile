# Use official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file first (leverages Docker cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
