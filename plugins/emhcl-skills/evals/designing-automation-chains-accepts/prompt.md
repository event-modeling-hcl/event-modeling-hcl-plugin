---
description: Acceptance of automation chain design on a small inline model.
tags: [method, structure]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Model facts:
- External system Shipping Carrier sends the event "Parcel Delivered" (external context).
- Internal events: Order Shipped, Order Delivered, Review Requested.
- The business wants: when a parcel is delivered, record that the order was delivered. Three days after delivery, ask the customer for a review, unless the order was returned.
- Internal event Order Returned exists.
Design the automations.
