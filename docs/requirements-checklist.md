# Requirements checklist

Every requirement and required output from the assessment brief, in the brief's own order. Fill in the last three columns as you build: by the deadline every row should point to working code and to a test. The wording here is a summary: **the brief is the authority.**

## The system (rules and requirements)

| ID | The brief requires | Where in my system | Test (from `test-plan.md`) | Done |
|---|---|---|---|---|
| R1 | Patients grouped into Low, Medium and High risk, from their condition(s) and history | | | [ ] |
| R2 | Sensor readings ingested continuously for each patient through an IoT-style feed (simulation is allowed) | | | [ ] |
| R3 | A machine learning model classifies each reading (or sequence of readings) as Normal, Warning or Critical | | | [ ] |
| R4 | A Critical reading triggers an automated alert to the assigned clinician, with patient ID, the vitals and a timestamp | | | [ ] |
| R5 | Data stored securely and access-controlled: clinicians see only their own patients; a patient view (if built) shows only that patient | | | [ ] |
| R6 | A history of readings and alerts is kept for each patient, for trends over time | | | [ ] |
| R7 | Data protection and confidentiality respected (e.g. UK GDPR); no real patient data at any stage | | | [ ] |
| R8 | Vital-sign trends shown over time (dashboard charts) | | | [ ] |
| R9 | Missing, delayed or anomalous readings handled gracefully, without false or missing alerts | | | [ ] |
| R10 | An admin or clinician view to set alert thresholds for each patient | | | [ ] |
| R11 | An architecture that uses emerging-technology principles (edge/cloud split, APIs, microservices, containers), with choices justified | | | [ ] |

## What you hand in (required outputs)

| ID | The brief requires | Outcome | Where | Done |
|---|---|---|---|---|
| Output 1 | A critical evaluation of at least two approaches (e.g. model types, or edge versus cloud), justifying your choice | LO1 | `docs/approaches.md`, report | [ ] |
| Output 2 | A working IPMS: IoT-style ingestion, a trained and evaluated model, a clinician dashboard, in an appropriate architecture | LO2 | repository, demo | [ ] |
| Output 3 | The ethical, security, privacy, sustainability and societal implications, and how your design addresses them | LO3 | `docs/ethics-security-checklist.md`, report | [ ] |
| Output 4 | Thorough testing, including model metrics (accuracy, precision, recall, F1, confusion matrix), with screenshots and test cases | | `docs/test-plan.md`, `docs/results/` | [ ] |
| Output 5 | A professional technical report with Harvard referencing: design, data and model decisions, assumptions, testing, limitations | LO3, LO4 | `docs/report/` | [ ] |
| Output 6 | A 10-minute presentation and demonstration of your working system | LO4 | `docs/report/presentation-plan.md` | [ ] |
