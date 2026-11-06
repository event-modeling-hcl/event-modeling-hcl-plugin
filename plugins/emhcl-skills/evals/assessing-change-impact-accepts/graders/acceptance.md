---
type: llm
---
PASS if each slice of the assessment appears once, in flow order, with exactly one status of existing, changed, or new (for example Return Bike changed, a new list of damaged bikes as new), and new slices are not grouped at the end, AND each changed slice lists its changes one line each and each new slice starts its description with "Proposed:" and has a sketch with its kind, fields, and a plain screen description. FAIL if a slice has no status or two statuses, steps are grouped by status, a new slice has no sketch, or a new slice reads as decided instead of proposed.
