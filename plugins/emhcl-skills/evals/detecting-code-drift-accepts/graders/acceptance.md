---
type: llm
---

PASS if the report walks the three commits one at a time, oldest first, lists 71f3a40 as noise and not as a finding, and reports no finding that comes from the model side only. PASS also requires that each finding has a kind, the commit, the file with its line, the element, a severity, and a proposed fix that names the model part it changes, and that the rename fix names both screens 'Book a Room' and 'My Booking'. FAIL if the agent judges only from the total difference, reports the dependency update as a finding, writes requests or a new code evidence source before the person confirms, or edits the code.
