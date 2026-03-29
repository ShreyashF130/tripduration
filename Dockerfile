FROM python:3.13.4

WORKDIR /app

# 1. Copy ONLY requirements first
COPY requirements.txt /app/requirements.txt

# 2. Install dependencies (Docker will cache this step!)
RUN pip install -r requirements.txt

# 3. NOW copy the rest of your heavy files and code
COPY app.py /app/app.py
COPY model.joblib /app/model.joblib
COPY src/ /app/src/

# 4. The starting command (with the space!)
CMD ["python", "app.py"]