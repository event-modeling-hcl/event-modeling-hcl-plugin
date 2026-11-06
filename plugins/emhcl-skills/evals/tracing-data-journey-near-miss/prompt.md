---
description: A check of the origin of every field belongs to the field lineage audit.
tags: [method, explanation]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Check every field in `rental.em.hcl` for a valid origin and report each field whose source is missing or wrong.
