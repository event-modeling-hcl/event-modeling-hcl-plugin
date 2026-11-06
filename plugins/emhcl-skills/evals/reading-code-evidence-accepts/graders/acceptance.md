---
type: llm
---

PASS if each evidence record or ledger row that the agent proposes has a code location with a path from the code root and a line (for example src/rental/RentalHandler.kt:42) and a certainty, and the agent records the pass as one evidence source of kind code whose location names rental-app/ and the short commit 9ab12cd, with a description that names the date, pass number, scope, and result. PASS also requires that the unused DELETE route becomes an open question rather than an element. FAIL if a location is vague (for example 'the rental code'), if the pass is not recorded as a code evidence source with the commit, if the agent writes events, commands, or screens directly instead of requests, or if it writes a ledger or history file beside the model.
