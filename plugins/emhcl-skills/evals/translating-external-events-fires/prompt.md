---
description: A user asks for translating external events in plain words.
tags: [method, structure]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

The payment provider sends us a charge.succeeded webhook with its own charge id, amount in cents, and a unix timestamp. Our translation step already records Rental Paid. Map the webhook fields into our event and tell me how to deal with duplicate deliveries.
