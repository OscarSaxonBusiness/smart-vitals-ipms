# ADR 2: Widen the systolic blood pressure limit to 40

**Status:** accepted
**Date:** 17 Nov 2026

## Context
The API throws away any impossible readings that are outside the sensor limits which should mean that glitches don't create any false alarms (R9). The simulator test then showed 3 real Critical readings (systolic 54, 58, 59) which were thrown away, due to the lower limit being 60. This meant that the patients in danger got no alert (R4).

## Options considered
1. Keep 60: fewer odd values get in, but real emergencies are missed.
2. Lower to 40: catches dangerously low blood pressure, and still rejects values that are almost certainly sensor faults.
3. Remove the limit: no missed readings, but glitches reach the model and cause false alarms.

## Decision
Option 2: lower the systolic limit to 40.

## Evidence
| | Limit 60 | Limit 40 |
|---|---|---|
| Critical readings missed | 3 | 0 |
| Real readings rejected | 3 | 0 |
| Alerts on sensor glitches | 0 | 0 |
| Duplicate alerts | 0 | 0 |

All 17 tests still pass.

## Consequences
- **Better:** no real Critical readings are thrown away, and glitches are still blocked.
- **Worse:** a faulty sensor reading between 40 and 60 could now get through. The model will judge it, and the clinician can check the trend on the dashboard.