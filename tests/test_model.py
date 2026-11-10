"""Run from the project folder with:  pytest
Checks that the saved model loads, answers with one of its labels, and copes with a missing reading (R9)."""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "first_model.joblib"
INFO = ROOT / "models" / "first_model.json"


@pytest.fixture(scope="module")
def saved():
    if not MODEL.exists():
        pytest.skip("no saved model yet: run notebooks/01_first_model.ipynb up to Step 8")
    return joblib.load(MODEL), json.loads(INFO.read_text())


def example(info):
    return pd.DataFrame([info["example_row"]], columns=info["features"]).astype(float)


def test_answers_with_a_known_label(saved):
    model, info = saved
    answer = model.predict(example(info))
    assert len(answer) == 1 and answer[0] in info["labels"]


def test_handles_a_missing_reading(saved):
    """R9: a sensor dropout must not crash the model."""
    model, info = saved
    row = example(info)
    row.iloc[0, row.columns.get_loc(info["features"][-1])] = np.nan
    assert model.predict(row)[0] in info["labels"]
