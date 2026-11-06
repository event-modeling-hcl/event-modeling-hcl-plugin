---
type: llm
---

PASS if both of these hold:
1. For Rent Kayak and Return Kayak, the reply addresses the command cases (happy path, variant, refused input, state violation, business duplicate, limit, authorization, alternative path, external failure, compensation): each case has a scenario or a stated reason why the domain excludes it.
2. Each of the three handbook rules has at least one scenario: a rejection for renting a kayak that is out, a rejection for returning a kayak that is not out, and the late fee limit with one scenario just under 4 hours (no fee) and one just over 4 hours (10 euros).
FAIL if any case is silently skipped, or if any of the three rules has no scenario.
