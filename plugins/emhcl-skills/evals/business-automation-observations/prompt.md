---
description: Exercise business automation observations.
tags: [business, acceptance, migration]
max_turns: 25
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Write faithful business scenarios for this agreed workshop model; do not encode HCL or run tools. Orders records Order Placed(order_id). An internal automation's pending-work list contains placed orders without Order Confirmation Requested. For a row on that list, its processor issues Request Order Confirmation(order_id), which records Order Confirmation Requested(order_id). Agreed cases: (1) Order Placed O-17 puts O-17 on the pending list; (2) when the processor handles that row it issues Request Order Confirmation O-17 and the command records Order Confirmation Requested O-17; (3) after both facts O-17 is absent from the pending list; (4) when the processor next checks the now-empty list, no command is dispatched. Keep the last case as business behavior, not a rejection or new failure event. Separate the automation's dispatch decision, command outcome, and list observations where that makes them clearer.
