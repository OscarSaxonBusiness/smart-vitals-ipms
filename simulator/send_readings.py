"""Smart Vitals simulator (requirement 2): sends readings to the API, the way patients' phones would.

Run it on your own computer, with the API running:   python -m simulator.send_readings
In a container, API_URL points at the api service instead of localhost (see docker-compose.yml).

Settings (environment variables):
  API_URL   where the API is              (default: http://localhost:8000)
  MINUTES   how many minutes to simulate  (default: 30)
  FAULTS    "on" adds dropouts, glitches, late readings and resent copies (default: on)
  SPEED     seconds to wait between readings; 0 = as fast as possible (default: 0)
"""
import json
import os
import random
import time
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import requests

API_URL = os.environ.get("API_URL", "http://localhost:8000")
MINUTES = int(os.environ.get("MINUTES", 30))
FAULTS = os.environ.get("FAULTS", "on") == "on"
SPEED = float(os.environ.get("SPEED", 0))
PATIENTS = json.loads((Path(__file__).resolve().parents[1] / "data" / "patients.json").read_text())


def teaching_status(heart, spo2, systolic, temp, glucose):
    """The points rule used to label simulated readings (invented for teaching; not a clinical score)."""
    points = ((2 if heart < 50 or heart > 120 else 1 if heart > 100 else 0)
              + (3 if spo2 < 91 else 1 if spo2 < 94 else 0)
              + (3 if systolic < 90 or systolic > 200 else 1 if systolic < 100 or systolic > 170 else 0)
              + (2 if temp > 39 or temp < 35.5 else 1 if temp > 38 else 0)
              + (0 if glucose is None else 3 if glucose < 70 or glucose > 300 else 1 if glucose > 220 else 0))
    return "Critical" if points >= 3 else "Warning" if points >= 1 else "Normal"


def make_readings(seed=8):
    """Readings for every patient, in the order they arrive, each with its true status."""
    rs = np.random.RandomState(seed)
    start = datetime(2026, 11, 10, 9, 0)
    out = []
    for pid, p in PATIENTS.items():
        base_hr, base_sys = rs.normal(72, 7), rs.normal(118, 9) + 6 * p["risk_level"]
        k = np.zeros(MINUTES)
        if rs.rand() < 0.10 * p["risk_level"] + 0.05:                  # an unwell spell
            s0 = rs.randint(0, max(1, MINUTES - 12))
            k[s0:s0 + rs.randint(6, 15)] = rs.uniform(0.6, 1.4)
        for m in range(MINUTES):
            heart = base_hr + rs.normal(0, 6) + k[m] * rs.choice([-22, 38])
            spo2 = min(100, rs.normal(97, 1.1) - k[m] * rs.uniform(2, 7))
            systolic = base_sys + rs.normal(0, 8) + k[m] * rs.choice([-35, 55])
            temp = rs.normal(36.8, 0.3) + k[m] * rs.uniform(0, 2.2)
            glucose = round(rs.normal(135, 25) + k[m] * rs.choice([-45, 150])) if p["diabetic"] else None
            t = start + timedelta(minutes=m)
            r = {"reading_id": f"{pid}-{m + 1:03d}", "patient_id": pid, "time": t.isoformat(timespec="seconds"),
                 "heart_rate": round(heart), "spo2": round(spo2, 1), "systolic_bp": round(systolic),
                 "diastolic_bp": round(0.55 * systolic + rs.normal(12, 5)), "temperature": round(temp, 1), "glucose": glucose}
            truth, arrives, fault = teaching_status(heart, spo2, systolic, temp, glucose), t, ""
            if FAULTS:
                u = rs.rand()
                if u < 0.01:
                    r["heart_rate"], truth, fault = 250, "sensor error", "glitch"
                elif u < 0.04:
                    r[["heart_rate", "spo2", "systolic_bp", "temperature"][rs.randint(4)]] = None
                if rs.rand() < 0.02:
                    arrives += timedelta(minutes=5)
            out.append((arrives, r, truth, fault))
            if FAULTS and rs.rand() < 0.03:
                out.append((arrives + timedelta(seconds=10), r, truth, "resend"))
    if FAULTS:
        out.append((start, {**out[0][1], "reading_id": "P099-001", "patient_id": "P099"}, "unknown", "stranger"))
    return [(r, truth, fault) for _, r, truth, fault in sorted(out, key=lambda x: x[0])]


def backoff_delay(attempt, base=0.5, cap=8.0):
    """Week 7: wait longer after each failed try, with jitter so phones do not all retry together."""
    return random.uniform(0, min(___, base * 2 ** ___))       # TODO: never longer than cap; doubles with each attempt


def send(reading, tries=6):
    """POST one reading. If the API cannot be reached, back off and try again."""
    for attempt in range(tries):
        try:
            reply = requests.post(f"{API_URL}/readings", json=reading, timeout=5)
            return reply.status_code, reply.json()
        except requests.exceptions.RequestException:
            time.sleep(backoff_delay(attempt))
    return "gave up", {}


def wait_for_api(tries=10):
    for attempt in range(tries):
        try:
            if requests.get(f"{API_URL}/health", timeout=3).ok:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(backoff_delay(attempt))
    return False


def main():
    print(f"Simulator: {len(PATIENTS)} patients, {MINUTES} minutes, faults {'on' if FAULTS else 'off'}, API at {API_URL}", flush=True)
    if not wait_for_api():
        print("The API did not answer /health. Is it running?", flush=True)
        return
    readings = make_readings()
    codes, ms, real_rejected = Counter(), [], []
    began = time.perf_counter()
    for reading, truth, fault in readings:
        t0 = time.perf_counter()
        code, body = send(reading)
        ms.append((time.perf_counter() - t0) * 1000)
        codes[code] += 1
        if code == 422 and truth != "sensor error":         # a REAL reading the API threw away
            real_rejected.append((reading["reading_id"], truth, body.get("problems")))
        time.sleep(SPEED)
    took = time.perf_counter() - began
    alerts = [a for c in sorted({p["clinician"] for p in PATIENTS.values()})
              for a in requests.get(f"{API_URL}/alerts", params={"clinician": c}, headers={"X-Clinician-ID": c}, timeout=5).json()]
    alerted = [f"{a['patient_id']}@{a['time']}" for a in alerts]
    key = lambda r: f"{r['patient_id']}@{r['time']}"
    critical = {key(r) for r, truth, _ in readings if truth == "Critical"}
    glitches = {key(r) for r, _, fault in readings if fault == "glitch"}
    print(f"Sent {len(readings)} readings in {took:.1f} s ({len(readings) / took:.0f} per second)")
    print("Replies:", {str(k): v for k, v in sorted(codes.items(), key=str)})
    print(f"Alerts on the API: {len(alerts)} | duplicate alerts: {len(alerted) - len(set(alerted))} | "
          f"alerts on sensor glitches: {len(set(alerted) & glitches)} | Critical readings missed: {len(critical - set(alerted))}")
    print(f"Real readings rejected as impossible: {len(real_rejected)}")
    for rid, truth, problems in real_rejected:
        print(f"   {rid} (truly {truth}): {problems}")
    print(f"Response time: median {np.median(ms):.1f} ms, p95 {np.percentile(ms, 95):.1f} ms", flush=True)


if __name__ == "__main__":
    main()
