---
description: A request close to designing automation chains that belongs to translating external events.
tags: [method, structure]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Here is the JSON that the payment provider posts to us: {"id":"ch_1","amount":900,"currency":"eur"}. How do these fields map to our Rental Paid event, and how do we link the charge id to our rental?
