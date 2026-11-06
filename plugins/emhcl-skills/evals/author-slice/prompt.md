---
description: Write a new single-file model with a state change slice. Needs --allow-tools Write.
tags: [language, write]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Write, Glob, Grep, Skill]
---

Write an Event Modeling HCL model to the file cancel.em.hcl in the current folder. A pet owner opens the appointment screen and cancels an appointment. The system records that the appointment was cancelled, with the appointment ID and the cancellation reason. Do not explain the language, just write the file.
