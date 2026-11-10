# Ethics, security, privacy and sustainability checklist (Output 3, LO3)

Go through this now, and again before you hand in. Each item needs a sentence in your report: what the risk is, and what your design does about it.

## Data protection (R5, R7)
- [ ] No real patient data anywhere: simulated, synthetic or open and anonymised only.
- [ ] Health data is *special category* data under UK GDPR. Which principles would a real MedLink system have to meet (lawful basis, data minimisation, storage limitation, security)?
- [ ] Do I collect only the data the system needs?
- [ ] How long are readings and alerts kept, and who can delete them?

## Security (R5)
- [ ] Clinicians log in, and can see only their own patients. A patient view shows only that patient. Tested?
- [ ] Passwords are stored hashed, never in plain text; keys live in `.env`, not in the repository.
- [ ] Traffic between parts is encrypted (HTTPS, MQTT over TLS), or I explain why not in a prototype.
- [ ] Is there a log of who viewed or changed what?
- [ ] Where could someone attack the system: the feed, the API, the model, the dashboard? (Week 10)

## Safety and fairness
- [ ] Missed Critical (no alert) versus false alarm (alarm fatigue): which does my design favour, and why?
- [ ] Does the model work as well for every risk group, and for patients with and without diabetes?
- [ ] Does the clinician see how sure the model is, and why it raised an alert? The clinician, not the model, decides.
- [ ] Does my report say clearly that this is a prototype, not a medical device?

## Sustainability and society
- [ ] Roughly how much computing do training and running my system use? Could the edge, a smaller model or less frequent retraining do the job (Weeks 6 and 7)?
- [ ] Who could be left out: patients without a smartphone, good signal or digital skills?
- [ ] Have I declared where and how I used AI tools?
