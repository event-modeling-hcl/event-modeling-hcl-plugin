---
type: llm
---

PASS if both of these hold:
1. Every audit in the report has a status with evidence, or NOT RUN with the missing part named (for example no commands, no streams, no slices). No audit about commands, streams, read models, slices, or shapes is marked PASS.
2. The event audits run and find that Fine Total Calculated is a calculation (it belongs in a read model) and that Loan Maybe Overdue is not a fact that happened. The report says the run is partial.
FAIL if an audit whose input does not exist is marked PASS, or if either of the two event problems is missed.
