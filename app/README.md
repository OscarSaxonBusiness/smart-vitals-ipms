# app/ (R4, R5, R6, R11)

From Week 8: your API. It receives each reading, classifies it with your saved model, stores readings and alerts for each patient, and raises an alert when a reading is Critical.

Notebook 01 already saved what the API needs:
- `models/first_model.joblib`: the trained pipeline
- `models/first_model.json`: the column names, the labels and one example reading
