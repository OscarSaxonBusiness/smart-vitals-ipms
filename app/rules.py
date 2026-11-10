"""The rules the API applies to every reading. Copy your answers from the Week 8 class project."""

VITALS = ["heart_rate", "spo2", "systolic_bp", "diastolic_bp", "temperature", "glucose"]

# Values a sensor can really produce. Outside these = a sensor error.
# Heart rate widened from (30, 220) after the class project: a real heart rate of 28 was being thrown away.
LIMITS = {"heart_rate": (20, 240), "spo2": (70, 100), "systolic_bp": (60, 250),
          "diastolic_bp": (30, 150), "temperature": (30, 43), "glucose": (20, 600)}


def problems_in(reading):
    """A list of reasons to reject a reading (an empty list means it is fine)."""
    problems = []
    for name, (low, high) in LIMITS.items():
        value = reading.get(name)
        if value is None:            # a missing vital is allowed: the model fills the gap (requirement 9)
            continue
        if not (___ <= value <= ___):                         # TODO: the two limits (class project, Step 2a)
            problems.append(f"{name} = {value} is outside {low} to {high}")
    for field in ["reading_id", "patient_id", "time"]:
        if not reading.get(field):
            problems.append(f"{field} is missing")
    return problems


def already_stored(db, reading_id):
    """True if this reading was stored before: a resent copy."""
    row = db.execute("SELECT 1 FROM readings WHERE reading_id = ?", (___,)).fetchone()   # TODO: which ID? (Step 2b)
    return row is not ___                                                                  # TODO


def make_alert(reading, status, patient):
    """The alert the brief asks for (requirement 4): which patient, which clinician, the vitals and the time."""
    return {"patient_id": reading["patient_id"],
            "clinician_id": ___,                   # TODO: the patient's assigned clinician (Step 2c)
            "time": ___,                           # TODO: when the reading was taken
            "status": status,
            "vitals": {v: reading.get(v) for v in VITALS}}


def status_code(outcome):
    """The HTTP status code the API sends back for each outcome."""
    codes = {"created": ___,                   # TODO (Step 2c)
             "duplicate": ___,
             "invalid": ___,
             "unknown patient": ___}
    return codes[outcome]


def can_view(clinician_id, patient):
    """A clinician may see only their own patients (requirement 5). Switched on with CHECK_ACCESS=on."""
    return patient is not None and patient["clinician"] == ___         # TODO (Step 5c)
