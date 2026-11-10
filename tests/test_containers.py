"""Week 8 container checks. They read your files; they do not need Docker. Run:  pytest"""
from pathlib import Path

import sklearn
import yaml

ROOT = Path(__file__).resolve().parents[1]
FILES = ["app/Dockerfile", "simulator/Dockerfile", "docker-compose.yml", "app/requirements.txt", "app/rules.py", "simulator/send_readings.py"]


def text(name):
    return (ROOT / name).read_text()


def test_no_blanks_left():
    left = [f for f in FILES if "___" in text(f)]
    assert not left, f"replace every ___ in: {', '.join(left)}"


def test_api_image():
    d = text("app/Dockerfile")
    assert "FROM python:" in d, "start from an official Python image"
    assert "EXPOSE 8000" in d, "the API listens on port 8000"
    assert "app.main" in d, "the image should start the API (python -m app.main)"


def test_compose_services():
    compose = yaml.safe_load(text("docker-compose.yml"))
    assert {"api", "simulator"} <= set(compose["services"]), "you need an api service and a simulator service"
    assert compose["services"]["simulator"]["environment"]["API_URL"] == "http://api:8000", \
        "inside the compose network the simulator reaches the API by its service name"
    assert "8000:8000" in compose["services"]["api"]["ports"], "publish port 8000 so you can open it in a browser"


def test_model_version_pinned():
    line = next((l for l in text("app/requirements.txt").splitlines() if l.startswith("scikit-learn==")), "")
    assert line == f"scikit-learn=={sklearn.__version__}", \
        f"pin the scikit-learn that saved your model: scikit-learn=={sklearn.__version__} (found: {line or 'nothing'})"


def test_secrets_stay_out_of_images():
    assert ".env" in text(".dockerignore").split(), ".dockerignore must list .env so secrets never go into an image"
