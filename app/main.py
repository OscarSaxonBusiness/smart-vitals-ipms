"""Smart Vitals API (Week 8, Milestone 1).

Run it on your own computer:   python -m app.main
Then open:                     http://localhost:8000/health
In a container, the same command runs inside the image (see app/Dockerfile).

Settings come from environment variables, so the same code runs on a laptop and in a container:
  MODEL_PATH     the saved model from notebook 01   (default: models/first_model.joblib)
  PATIENTS_PATH  the patient register              (default: data/patients.json)
  DB_PATH        where readings and alerts are kept (default: smart_vitals.db)
  PORT           the port to listen on             (default: 8000)
  CHECK_ACCESS   "on": clinicians see only their own patients and alerts (default: off)
"""
import json
import os
import sqlite3
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, g, jsonify, request

from app.rules import already_stored, can_view, make_alert, problems_in, status_code

ROOT = Path(__file__).resolve().parents[1]


def create_app(model_path=None, patients_path=None, db_path=None):
    app = Flask(__name__)
    model_path = Path(model_path or os.environ.get("MODEL_PATH", ROOT / "models" / "first_model.joblib"))
    patients_path = Path(patients_path or os.environ.get("PATIENTS_PATH", ROOT / "data" / "patients.json"))
    db_path = str(db_path or os.environ.get("DB_PATH", ROOT / "smart_vitals.db"))
    check_access = os.environ.get("CHECK_ACCESS", "off") == "on"

    model = joblib.load(model_path)                                   # load the model ONCE, when the app starts
    info = json.loads(model_path.with_suffix(".json").read_text())    # the column names saved by notebook 01
    patients = json.loads(patients_path.read_text())

    def db():
        """One database connection per request; the data itself lives in a file (or a container volume)."""
        if "db" not in g:
            g.db = sqlite3.connect(db_path)
        return g.db

    @app.teardown_appcontext
    def close_db(error):
        connection = g.pop("db", None)
        if connection is not None:
            connection.close()

    with sqlite3.connect(db_path) as setup:
        setup.execute("CREATE TABLE IF NOT EXISTS readings (reading_id TEXT UNIQUE, patient_id TEXT, time TEXT, status TEXT, data TEXT)")
        setup.execute("CREATE TABLE IF NOT EXISTS alerts (alert_id INTEGER PRIMARY KEY, reading_id TEXT, patient_id TEXT, clinician_id TEXT, data TEXT)")

    @app.post("/readings")
    def receive_reading():
        reading = request.get_json(silent=True) or {}
        problems = problems_in(reading)
        if problems:
            return jsonify({"outcome": "invalid", "problems": problems}), status_code("invalid")
        patient = patients.get(reading["patient_id"])
        if patient is None:
            return jsonify({"outcome": "unknown patient"}), status_code("unknown patient")
        if already_stored(db(), reading["reading_id"]):
            return jsonify({"outcome": "duplicate", "reading_id": reading["reading_id"]}), status_code("duplicate")
        row = pd.DataFrame([{f: reading.get(f, patient.get(f)) for f in info["features"]}], columns=info["features"]).astype(float)
        status = str(model.predict(row)[0])
        try:
            db().execute("INSERT INTO readings VALUES (?, ?, ?, ?, ?)",
                         (reading["reading_id"], reading["patient_id"], reading["time"], status, json.dumps(reading)))
        except sqlite3.IntegrityError:          # another copy of the API stored it a moment ago
            return jsonify({"outcome": "duplicate", "reading_id": reading["reading_id"]}), status_code("duplicate")
        alert = None
        if status == "Critical":
            alert = make_alert(reading, status, patient)
            db().execute("INSERT INTO alerts (reading_id, patient_id, clinician_id, data) VALUES (?, ?, ?, ?)",
                         (reading["reading_id"], reading["patient_id"], alert["clinician_id"], json.dumps(alert)))
            print(f"ALERT to {alert['clinician_id']}: {reading['patient_id']} is Critical at {reading['time']}", flush=True)
        db().commit()
        return jsonify({"outcome": "created", "reading_id": reading["reading_id"], "status": status,
                        "alert": alert is not None}), status_code("created")

    @app.get("/patients/<patient_id>/readings")
    def patient_history(patient_id):
        if check_access and not can_view(request.headers.get("X-Clinician-ID"), patients.get(patient_id)):
            return jsonify({"outcome": "forbidden"}), 403
        rows = db().execute("SELECT time, status, data FROM readings WHERE patient_id = ? ORDER BY time", (patient_id,)).fetchall()
        return jsonify([{**json.loads(data), "status": status} for _, status, data in rows])

    @app.get("/alerts")
    def list_alerts():
        clinician = request.args.get("clinician", "")
        if check_access and request.headers.get("X-Clinician-ID") != clinician:     # only your own alerts
            return jsonify({"outcome": "forbidden"}), 403
        rows = db().execute("SELECT data FROM alerts WHERE clinician_id = ?", (clinician,)).fetchall()
        return jsonify([json.loads(data) for (data,) in rows])

    @app.get("/health")
    def health():
        stored = db().execute("SELECT COUNT(*) FROM readings").fetchone()[0]
        return jsonify({"status": "ok", "labels": info["labels"], "readings_stored": stored})

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
