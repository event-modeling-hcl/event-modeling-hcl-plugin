---
description: Asks which aggregate each event belongs to; must load the streams skill.
tags: [method, discovery]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

In our library model, which aggregate or stream should each event go to? Events: Book Lent, Loan Extended, Book Returned, Member Joined, Address Changed, Fine Charged. I am also unsure whether we need an "All Loans" stream.
