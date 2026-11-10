# Test plan (Output 4)

Write the tests **before** you build each part, then fill in the results with screenshots. Every requirement in `requirements-checklist.md` should have at least one test. This becomes your test evidence for the report.

| ID | Requirement | What I do | Expected | Result and evidence | Pass? |
|---|---|---|---|---|---|
| T1 | R2 | Run the simulator for 10 patients for 10 minutes | 100 readings stored | | |
| T2 | R3 | Notebook 01 Step 7 on unseen patients | Recall for Critical at least my target | | |
| T3 | R4 | Send one Critical reading for patient P001 | One alert to P001's clinician, with patient ID, vitals and timestamp | | |
| T4 | R5 | Clinician A asks for a patient of clinician B | Refused (e.g. HTTP 403) | | |
| T5 | R6 | Ask for P001's history | All readings and alerts, in time order | | |
| T6 | R8 | Open P001 on the dashboard | Trend chart of each vital sign | | |
| T7 | R9 | One reading arrives with a vital missing (sensor dropout) | No crash, no false alert | | |
| T8 | R9 | A reading arrives 5 minutes late | Stored in the right time order, no duplicate alert | | |
| T9 | R9 | An impossible value arrives (e.g. heart rate 250) | Flagged as a sensor error, no Critical alert | | |
| T10 | R9 | The same message arrives twice (MQTT QoS 1) | One alert only (Week 7: idempotency) | | |
| T11 | R10 | Change the threshold for P001 only | Alerts change for P001, not for other patients | | |
| T12 | R11 | `docker compose up` on a clean machine | All services start; the API answers | | |

Automatic tests live in `tests/` and run with `pytest`. Add one each time you find a bug, so it cannot come back.
