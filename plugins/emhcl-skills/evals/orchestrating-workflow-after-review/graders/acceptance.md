---
type: llm
---

Judge the actual answer and actions, not the source text or exact skill names.

PASS only if the coordinator treats the clean review as completion of the reviews gate, not termination of the complete modeling run. It continues with the writers for slice status, ownership, and chapter summaries in that order. It preserves the requested planned status, Reservations ownership, and existing business meaning. It does not write model parts itself or invent missing business rules. Whole-run success requires every required gate to pass. A blocker must be reported as incomplete rather than successful.

FAIL if the answer stops solely because the review found nothing new, skips a remaining required part, or claims that the complete model is ready while those gates fail.
