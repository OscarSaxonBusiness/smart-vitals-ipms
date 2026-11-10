# API contract (Week 8)

The agreement between your API and everything that talks to it: the simulator, the dashboard, and later the alert service. Update it whenever an endpoint changes.

| Method and path | What it does | Success code | Error codes | Requirement |
|---|---|---|---|---|
| `POST /readings` | | | | R2, R4, R9 |
| `GET /patients/{id}/readings` | | | | R6, R5 |
| `GET /alerts?clinician=` | | | | R4 |
| `GET /health` | | | | R11 |

## One example request and reply
```
POST /readings
{ ... }

201
{ ... }
```
