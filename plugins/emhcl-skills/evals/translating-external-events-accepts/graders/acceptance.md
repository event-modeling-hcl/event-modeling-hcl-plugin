---
type: llm
---

PASS if the reply maps every payload field (tracking, ts, signed_by) to a business field of Order Delivered with a sample payload shown or referenced, AND it states a correlation method on our side (lookup of the order number by the stored tracking number) and keeps the tracking number as a plain field, never as the domain key. FAIL if a payload field is left unmapped without a reason, if the tracking number becomes the key of the order, or if correlation depends on the courier knowing our order number.
