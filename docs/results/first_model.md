# First model results (10 Nov 2026)

- Data: `demo_vitals.csv` (1800 rows, 8 feature columns)
- Predicting: `status`
- Test set: 360 rows, from 12 patients the model never saw

| Measure | Baseline | First model |
|---|---|---|
| accuracy | 0.758 | 0.933 |
| balanced accuracy | 0.333 | 0.847 |
| precision (macro) | 0.253 | 0.834 |
| recall (macro) | 0.333 | 0.847 |
| F1 (macro) | 0.288 | 0.837 |
| recall: Critical | 0.0 | 0.814 |

My target: Recall for critical of at least 0.9 on patients new to the model
