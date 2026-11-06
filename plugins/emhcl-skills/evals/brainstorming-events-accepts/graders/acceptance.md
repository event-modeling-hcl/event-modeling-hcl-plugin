---
type: llm
---

PASS if every event in the response has a past-tense business name (for example Appointment Booked, Appointment Rescheduled, Treatment Recorded, Claim Submitted, Claim Approved, Claim Rejected), each event carries an identity field, and no event holds a computed value: the total amount owed is treated as a read model or left out, not as an event, and there is no record-change event such as "Patient Record Updated". FAIL if any event is not in the past tense, if an event carries the patient total owed, or if a generic update event stays in the list.
