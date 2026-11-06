---
description: Acceptance of read model derivation on a small inline model.
tags: [method, structure]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Model facts:
- Screen "Library Account" for the Member shows: the number of books on loan, and a list of loans with title and due date. Read models named by the screen: Loans Of Member (planned).
- Events: Book Lent (loan number, member number, title, due date), Loan Extended (loan number, new due date), Book Returned (loan number).
- Screen "Join Library" is a blank sign-up form.
Derive the read models.
