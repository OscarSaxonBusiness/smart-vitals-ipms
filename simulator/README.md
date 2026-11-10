# simulator/ (R2, R9)

Your IoT-style sensor feed. Real hardware is not required: the brief allows readings to be simulated in software.

Start from your Week 4 and Week 6 code:
- one stream per patient, for example one reading a minute, with the five vital signs (glucose only for patients with diabetes) and each patient's risk group (R1)
- problems built in on purpose, so you can test R9: dropouts, delayed readings, impossible values and duplicate messages
- send readings to your API (Week 8), or publish them over MQTT (Week 6)

Record how it works, and its limits, in `data/DATA_CARD.md`.
