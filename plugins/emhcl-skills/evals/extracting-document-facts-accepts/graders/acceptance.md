---
type: llm
---

PASS if the reply contains a ledger in which each fact has an id, a kind, a statement, a location with section and page (for example 'section 2.2, page 4'), and a certainty, and no item that the agent assumed (such as the perspective) is labeled stated. PASS also requires that each event, deadline, rule, and requirement (the booking, the 24 hours, the 8 kg limit, the return time) is covered by evidence, a request for a model part, an open question, or a left-out decision with a reason, that the 72 versus 48 hours contradiction is one open question naming both locations, and that section 7 is left out with a reason. FAIL if any fact lacks a location or certainty, if an assumption is labeled stated, if the agent picks 72 or 48 hours without a question, if a fact is silently dropped, or if the agent writes a ledger file instead of putting the table in the reply.
