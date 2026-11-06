---
description: Asks for the state machine of a stream; must load the lifecycles skill.
tags: [method, discovery]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Our Booking stream in the hotel model has the events Booking Opened, Booking Confirmed, Booking Canceled, Stay Started, Stay Ended. Give me its state machine: states, which action moves it where, which actions are refused in which state, and the end states.
