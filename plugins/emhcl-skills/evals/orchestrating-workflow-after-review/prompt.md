---
description: Continue after a clean review until delivery gates pass.
tags: [method, process, acceptance]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Continue this complete modeling run from its supplied gate state. Give the next writer responsibilities in order and the whole-run stopping condition. Do not write files or run CLI commands.

The review just finished and found nothing new. Every gate before reviews passes. The slice-status, ownership, and chapter-summary gates still fail. The model has one slice, Reserve Seat, and one complete chapter, Seat Reservations. The requested status is planned. The owner is the Reservations team, which already exists in the model. The chapter summary must describe the already agreed reservation behavior. The person explicitly approves these remaining changes to Reserve Seat and its chapter. No permission or business decision blocks the remaining work.

The person asks to finish the complete model, not to stop after its review. Do not invent more business rules or declare that missing delivery parts are accepted debt.
