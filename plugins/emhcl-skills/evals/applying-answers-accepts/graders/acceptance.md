---
type: llm
---

PASS if the capacity answer becomes a decision naming Mia plus a request on Book Class concerning command scenarios (12 bookings, then refused), with the question class_capacity kept and marked resolved, and every request traces to one answer. PASS also requires that the cancel answer, which contradicts the one-hour scenario, becomes a question back with options and gets no decision or request, and that reminder_time stays open. FAIL if the agent edits commands, scenarios, or other elements directly, deletes a question, changes the model for the contradiction, or closes the unanswered question.
