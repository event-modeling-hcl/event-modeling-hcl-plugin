---
description: Audits an early events-only model as a partial audit.
tags: [method, review]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Our library model has only events so far, no commands, streams, read models, or screens yet:

- Book Lent
- Book Returned
- Fine Total Calculated
- Loan Maybe Overdue
- Member Joined

Audit the model against the modeling rules and give me a verdict. Do not change anything.
