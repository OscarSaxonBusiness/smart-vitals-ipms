# The Smart Vitals simulator image: plays the part of the patients' phones.
FROM python:3.12-slim

WORKDIR /service
COPY simulator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY simulator/ simulator/
COPY data/patients.json data/patients.json

CMD ["python", "-m", "simulator.send_readings"]   # TODO: the module that runs the simulator
