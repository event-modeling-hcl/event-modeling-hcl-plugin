---
type: llm
---

PASS if both of these hold:
1. Each of the three slices (Rent Kayak, Return Kayak, Open Rentals) has a coverage value or a stated reason for no value.
2. Each value equals 100 times covered meaningful cases divided by meaningful cases, rounded down (for example 2 of 3 gives 66, not 67). Return Kayak and Open Rentals have no scenarios, so a value for them must be 0.
FAIL if a slice is missing from the report, if any value is rounded up, or if a technical case (malformed input, retries, identifiers) counts as covered or missing.
