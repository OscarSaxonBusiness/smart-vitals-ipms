# Start here: Smart Vitals

This is your repository for the CMS22301 assessment: the **Smart Vitals Intelligent Patient Monitoring System (IPMS)** for MedLink Community Health Trust.

**Deadline: Friday 11 December 2026, 4 pm.** Submit on Canvas: your **technical report** and a link to this **code repository**. You also give a **live 10-minute presentation and demonstration**.

Work through the list in order and tick each box as you go.

## Before your Week 8 session
- [ ] **Read the brief**, then open `docs/requirements-checklist.md`: every requirement you must meet, in one table.
- [ ] **Plan your data** (`data/DATA_CARD.md`): your own simulator, or an open, anonymised dataset. **Never real patient data.**
- [ ] **Write your design plan** in `docs/design-plan.md` (or on the design plan form) and hand it in.
- [ ] **Run `notebooks/01_first_model.ipynb`**: a baseline, a first model tested on unseen patients, a saved model.
- [ ] **Fill in ADR 1** (`docs/adr/0001-first-model.md`) and start your **assumptions log** (`docs/assumptions.md`).
- [ ] **Log your week** in `docs/progress-log.md`, then commit and push.

## Every week after that
- [ ] Reach that week's milestone (see *Starting your Smart Vitals project*), tick off requirements in the checklist, add one line to the progress log, and commit at least once.

## What is where

| Folder or file | What goes in it | Brief |
|---|---|---|
| `README.md` | What your system does and how to run it: the front page of your submission | |
| `data/` | Your data card and data (simulated or open). `demo_vitals.csv` is practice data | R2, R7 |
| `simulator/` | Your IoT-style sensor feed | R2, R9 |
| `notebooks/` | Model experiments, numbered: `01_first_model`, `02_...` | R3, Outputs 1 and 4 |
| `src/` | Code you reuse, as functions (cleaning, features) | |
| `app/` | Your API: receives readings, classifies them, stores them, raises alerts (from Week 8) | R4, R5, R6, R11 |
| `dashboard/` | The clinician-facing dashboard | R5, R8, R10 |
| `models/` | Saved models and their description files | R3 |
| `tests/` | Automatic tests. Run them with `pytest` | Output 4 |
| `docs/` | Checklist, design plan, approaches, assumptions, ADRs, ethics and security, test plan, results, progress log, report | Outputs 1 to 6 |

## Four rules
1. **No real patient data, ever** (brief, requirement 7). Simulated, synthetic, or open and anonymised data only.
2. **No passwords or API keys in the repository.** Keep them in a `.env` file: Git ignores it.
3. **Commit little and often**, with messages that say what changed: "Add Critical alert to API" beats "update".
4. **Say where code came from.** Reusing your weekly lab code, a library example or AI-generated suggestions must be acknowledged in the code and the README, following the university's rules on academic misconduct and the use of AI.
