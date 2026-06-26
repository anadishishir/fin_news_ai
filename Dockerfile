# 1. Using An Official Lightweight Python Base Image 
FROM python:3.11-slim 

# 2. Setting The Working Directory Inside The Container 
WORKDIR /app 

# 3. Installing System - Level Dependencies Required For Scientific Libraries 
RUN apt-get update && apt-get install -y --no-install-recommends \ 
    build-essential \ 
    && rm -rf /var/lib/apt/lists/* 

# 4. Copying And Installing Dependencies First (Docker Cache Optimization) 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt 

# 5. Copying The Rest Of Our Application Code 
COPY . . 

# 6. Exposing The Port That Streamlit Uses 
EXPOSE 8501 

# 7. Defining The Command To Run Our App 
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"] 