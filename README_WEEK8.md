# Week 8 · Milestone 1: Smart Vitals as a containerised service

These files turn your Smart Vitals model into a **service**: an API that validates, classifies, stores and alerts, plus a simulator that sends it readings, each in its own container.

Full instructions and the marking guide are in **Week8_Assignment_Brief**. This page is the quick version.

## 1 · Put the files in your repository

Copy everything in this folder into the **root** of your `smart-vitals-ipms` repository (the one from the start kit). It adds:

```
app/            the API (main.py) and its rules (rules.py)  <- you finish rules.py
simulator/      sends readings, the way patients' phones would
data/patients.json   20 patients and their clinicians (simulated)
tests/          15 Week 8 tests
docker-compose.yml, .dockerignore, app/Dockerfile, simulator/Dockerfile   <- you fill the blanks
docs/api.md     your API contract                         <- you complete it
```

You also need `models/first_model.joblib` and `models/first_model.json` from notebook 01. If they are missing, run notebook 01 again.

Install what the tests need (once): `pip install flask pandas joblib scikit-learn requests pytest pyyaml`

## 2 · Make the API work (no Docker needed)

1. Open `app/rules.py`. Replace every `___` with your answers from the **class project** (Steps 2a to 2c and 5c).
   Then finish `backoff_delay` in `simulator/send_readings.py` (Week 7: exponential backoff with jitter).
2. Run `pytest tests/test_api.py tests/test_simulator.py`. All 10 should pass.
3. Start the API: `python -m app.main`, then open <http://localhost:8000/health> in a browser.
4. In a **second** terminal: `python -m simulator.send_readings`. Save the summary it prints.

## 3 · Put it in containers

1. Fill the blanks in `app/Dockerfile`, `simulator/Dockerfile`, `docker-compose.yml` and `app/requirements.txt`.
   For the scikit-learn version, run `python -c "import sklearn; print(sklearn.__version__)"` where you ran notebook 01.
2. Run `pytest`. All tests should pass, including the 5 container checks (these read your files; they do not need Docker).
3. Stop the API from step 2 (`Ctrl + C`), then run `docker compose up --build`.
   The simulator waits until the API is healthy, then sends its readings. If everything is right it reports **616 readings sent**.
4. Stop with `Ctrl + C`, then `docker compose down`. (`docker compose down -v` also deletes the stored readings.)

## Where to run Docker

* **Your own laptop:** Docker Desktop (Windows needs WSL 2). Free for education and personal use.
* **A lab PC:** ask in the session which rooms have Docker.
* **No Docker at all?** Steps 1 and 2 still work, and so do most tasks. Do the container steps on a lab PC.

## If something goes wrong

| You see | It means |
|---|---|
| `NameError: name '___' is not defined` | a blank is left in `app/rules.py` |
| `FileNotFoundError ... first_model.joblib` | run notebook 01 to save your model into `models/` |
| `port is already allocated` | the API from step 2 is still running: stop it with `Ctrl + C` |
| the simulator says `The API did not answer /health` | the API is not running, or `API_URL` is wrong |
| `InconsistentVersionWarning` | the scikit-learn in the image is not the one that saved your model: fix the pin |

All data is simulated for teaching. Never put real patient data in this repository or in an image.
