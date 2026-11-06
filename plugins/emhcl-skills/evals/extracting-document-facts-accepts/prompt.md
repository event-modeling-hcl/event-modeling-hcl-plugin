---
description: Acceptance of document fact extraction on a small inline input.
tags: [method, intake]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Pull the facts out of this excerpt of our service contract for an event model. The model is still empty. Do not ask me questions, take assumptions where needed. Show me the ledger.

```text
Service contract, laundry pickup, version 3 (file: contract-v3.pdf)

Section 2.1, page 4: The customer books a pickup in the app. The driver collects the bag within 24 hours after the booking.
Section 2.2, page 4: A bag weighs at most 8 kg. A heavier bag is refused at the door.
Section 2.3, page 5: Clean laundry is returned within 72 hours after pickup.
Section 2.3, page 9: Clean laundry is returned within 48 hours after pickup.
Section 7, page 12: General terms of liability apply as in annex B.
```
