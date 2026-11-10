# ADR 1: My first model, and the baseline it must beat

**Status:** proposed
**Date:** 10 Nov 2026

## Context
The model must classify each reading as Normal, Warning or Critical (R3). A missed Critical means no alert (R4); a false Critical is a false alarm (R9). Which mistake matters more for MedLink?

## Options considered
- A baseline with no learning (always the most common label)
- A straight-line model (logistic regression)
- A random forest

## Decision
Build on the random forest. It had the best recall for Critical and balanced accuracy.

## Evidence
Recall for Critical: baseline 0.000, logistic regression 0.746, random forest 0.814. Balanced accuracy 0.847 vs 0.627. On 12 unseen patients it missed 11 of 59 Critical readings (2 called Normal) and raised 4 false alarms. (Add the confusion matrix screenshot later.)

## Consequences
- **Better:** catches far more emergencies, with few false alarms.
- **Worse:** below my 0.90 target, and harder to explain than a straight line. I’ll add “why this alert?” explanations later.