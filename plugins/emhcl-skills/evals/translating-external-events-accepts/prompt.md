---
description: Acceptance of external event translation on a small inline model.
tags: [method, structure]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Model facts:
- External system Courier sends "delivery_confirmed": {"tracking":"TRK-88","ts":"2026-03-02T10:15:00Z","signed_by":"J. Doe"}.
- A translation step exists: todo list Courier Confirmations, command Record Delivery, internal event Order Delivered.
- Our command Ship Order stored the tracking number with the order number when it booked the courier.
- Order Delivered needs: order number, delivered at, recipient name, tracking number.
Map the payload.
