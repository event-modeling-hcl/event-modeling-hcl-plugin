---
description: A user asks to list slices with dependencies and set their status, which belongs to the slice planning skill.
tags: [method, delivery]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

The review of our library model is done. Go through the model, list every slice with the events it uses and produces and which slices come before and after it, and mark each slice as planned or blocked.
