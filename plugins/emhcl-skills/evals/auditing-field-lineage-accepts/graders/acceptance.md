---
type: llm
---

PASS if both of these hold:
1. The report covers the whole model (it names the workflows or chapters it audited, or the number of fields), not only one element.
2. The report finds that the command field pickup_date reaches no event (Cake Ordered lacks it), and that the event field price has no origin because the command does not carry it. The pickup_date gap is reported once at its origin, not again at Order List.
FAIL if either gap is missing, or if the pickup_date gap is reported separately at each downstream element.
