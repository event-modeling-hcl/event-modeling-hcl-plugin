---
type: llm
---

PASS if every automation in the reply reads its own todo list and every trigger is a real event in the model, AND the external event Parcel Delivered opens only a translation step (which records Order Delivered with no business decision and no closing event), with the review request as a separate worker step whose todo list internal events open. FAIL if an automation has no todo list, if Parcel Delivered opens the review worker directly, or if the translation step makes a decision or has a closing event.
