# The Smart Vitals API image (built from the repository root)
FROM python:3.12-slim                    

WORKDIR /service

# 1. Libraries first: reused until requirements change
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Then the code, the model and the patient register
COPY app/ app/
COPY models/ models/
COPY data/patients.json data/patients.json

ENV MODEL_PATH=/service/models/first_model.joblib \
    PATIENTS_PATH=/service/data/patients.json \
    DB_PATH=/data/smart_vitals.db

EXPOSE 8000                    
CMD ["python", "-m", "app.main"]   
