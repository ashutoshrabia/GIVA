# Start with a lightweight Python image—3.9-slim keeps it small but functional
FROM python:3.9-slim

# Set the working directory inside the container where our app will live
WORKDIR /app

# Copy the requirements file first—this helps Docker cache the install step
COPY requirements.txt .

# Install all the Python packages we need from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables to writable cache directories
ENV TRANSFORMERS_CACHE=/tmp/cache
ENV HF_HOME=/tmp/hf_home
ENV XDG_CACHE_HOME=/tmp/cache

# Create the directories if they don't exist
RUN mkdir -p /tmp/cache /tmp/hf_home

# Copy everything else in our project folder (app.py, Articles.csv) into the container
COPY . .

# Tell Docker how to run our app—start Uvicorn on port 7860 for Hugging Face
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
