---
description: Exercise hcl library authoring.
tags: [language, acceptance, migration]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Write, Edit, Bash, Glob, Grep, Skill]
---

Create `borrowing.em.hcl` for a library. A member uses a checkout screen to borrow an available book copy. Borrow Book produces Book Borrowed; reject an attempt when the copy is already on loan. Members can view their current loans. When a loan becomes overdue, the system should request an overdue notice without human input. Include UUID member_id and copy_id contracts, concrete Read Model questions, and scenarios. Write the file in the current directory and validate it if the Event Modeling HCL CLI is available.
