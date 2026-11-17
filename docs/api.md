# API contract

How other parts of the system (the simulator and the dashboard) talk to the API.

| Method and path | What it does | Success code | Error codes | Requirement |
|---|---|---|---|---|
| `POST /readings` | Checks the reading, ignores any duplicates, asks the model, saves it then alerts if it is Critical | 201 (200 if duplicate) | 422 invalid, 404 unknown patient | R2, R4, R9 |
| `GET /patients/{id}/readings` | Shows one patient's past readings | 200 | 403 not their clinician | R6, R5 |
| `GET /alerts?clinician=` | Lists all Critical alerts for one clinician | 200 | 403 not their alerts | R4 |
| `GET /health` | States if the API is running and then shows how many readings are stored | 200 | none | R11 |

## Example request and reply
```
POST /readings
{"reading_id": "P001-001", "patient_id": "P001", "time": "2026-11-17T09:00:00",
 "heart_rate": 72, "spo2": 98, "systolic_bp": 120, "diastolic_bp": 80, "temperature": 36.8}

201
{"outcome": "created", "reading_id": "P001-001", "status": "Normal", "alert": false}
```