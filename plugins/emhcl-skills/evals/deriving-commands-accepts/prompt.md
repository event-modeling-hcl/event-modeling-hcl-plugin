---
description: Acceptance of command derivation on a small inline model.
tags: [method, structure]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Model facts:
- Role: Member (human). System actor: Hold Expirer.
- Screen "Book a Court" for the Member, action "Book". Shows court and slot. Asks for court number and slot start.
- Stream: Court Booking, identity booking number. Lifecycle states: Held, Confirmed (end), Lapsed (end, cancel path).
- Events: Court Held, Booking Confirmed, Hold Lapsed.
- Rule: a hold lapses 10 minutes after it was made unless the member confirmed it. A slot in the past cannot be booked.
- Screen "My Hold" for the Member, action "Confirm".
Derive the commands.
