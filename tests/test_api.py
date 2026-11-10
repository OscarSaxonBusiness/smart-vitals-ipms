"""Week 8 API tests. Run from the project folder:  pytest
Each test checks one requirement from the brief. A test that fails with  NameError: name '___'  means a blank is left in app/rules.py."""
import json
from pathlib import Path

import pytest

from app.main import create_app

PATIENTS = json.loads((Path(__file__).resolve().parents[1] / "data" / "patients.json").read_text())


@pytest.fixture()
def client(tmp_path):
    """A fresh API with an empty database for every test. testing=True shows the real error instead of a 500."""
    app = create_app(db_path=tmp_path / "test.db")
    app.testing = True
    return app.test_client()


def reading(**changes):
    base = {"reading_id": "T-001", "patient_id": "P001", "time": "2026-11-10T09:00:00", "heart_rate": 75, "spo2": 97.0,
            "systolic_bp": 120, "diastolic_bp": 78, "temperature": 36.8, "glucose": None}
    return {**base, **changes}


CRITICAL = dict(heart_rate=135, spo2=82.0, systolic_bp=85, diastolic_bp=55, temperature=39.6)   # clearly Critical


def test_health(client):
    reply = client.get("/health")
    assert reply.status_code == 200 and reply.get_json()["status"] == "ok"


def test_new_reading_is_stored(client):
    reply = client.post("/readings", json=reading())
    assert reply.status_code == 201, f"a new reading should get 201, got {reply.status_code}"
    assert reply.get_json()["status"] in client.get("/health").get_json()["labels"]


def test_resent_copy_is_stored_once(client):                       # requirement 9: duplicates
    codes = [client.post("/readings", json=reading()).status_code for _ in range(2)]
    assert codes == [201, 200], f"the same reading twice should give 201 then 200, got {codes}"
    assert len(client.get("/patients/P001/readings").get_json()) == 1


def test_impossible_value_is_rejected(client):                     # requirement 9: anomalous readings
    reply = client.post("/readings", json=reading(heart_rate=300))
    assert reply.status_code == 422 and "heart_rate" in reply.get_json()["problems"][0]


def test_missing_vital_is_accepted(client):                         # requirement 9: missing readings
    assert client.post("/readings", json=reading(spo2=None)).status_code == 201


def test_unknown_patient(client):
    assert client.post("/readings", json=reading(patient_id="P999")).status_code == 404


def test_critical_reading_raises_one_alert(client):                 # requirement 4
    first = client.post("/readings", json=reading(**CRITICAL)).get_json()
    assert first["status"] == "Critical" and first["alert"], f"this reading should be Critical with an alert, got {first}"
    client.post("/readings", json=reading(**CRITICAL))            # resent copy: no second alert
    alerts = client.get("/alerts", query_string={"clinician": PATIENTS["P001"]["clinician"]}).get_json()
    assert len(alerts) == 1, f"one alert expected, got {len(alerts)}"
    assert {"patient_id", "clinician_id", "time", "vitals"} <= set(alerts[0]), "an alert needs patient, clinician, time and vitals"


def test_history_is_in_time_order(client):                          # requirement 6, with a late reading
    client.post("/readings", json=reading(reading_id="T-002", time="2026-11-10T09:05:00"))
    client.post("/readings", json=reading(reading_id="T-001", time="2026-11-10T09:00:00"))   # arrives late
    times = [r["time"] for r in client.get("/patients/P001/readings").get_json()]
    assert len(times) == 2, f"both readings should be stored, got {len(times)}"
    assert times == sorted(times), f"history should be in time order, got {times}"


def test_clinicians_see_only_their_own_patients(tmp_path, monkeypatch):   # requirement 5 (class project, Step 5c)
    monkeypatch.setenv("CHECK_ACCESS", "on")
    app = create_app(db_path=tmp_path / "access.db")
    app.testing = True
    client = app.test_client()
    client.post("/readings", json=reading())
    own = PATIENTS["P001"]["clinician"]
    other = next(c for c in ["C01", "C02", "C03", "C04"] if c != own)
    assert client.get("/patients/P001/readings", headers={"X-Clinician-ID": own}).status_code == 200
    assert client.get("/patients/P001/readings", headers={"X-Clinician-ID": other}).status_code == 403, \
        "another clinician must get 403 Forbidden"
    assert client.get("/alerts", query_string={"clinician": own}, headers={"X-Clinician-ID": other}).status_code == 403, \
        "nobody may read another clinician's alerts"
