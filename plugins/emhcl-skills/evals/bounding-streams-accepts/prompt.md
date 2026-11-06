---
description: Acceptance of the first two Done-when items of the bounding-streams skill on a small inline domain.
tags: [method, discovery]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Events of a car sharing model:

Car Added To Fleet (carId), Car Reserved (reservationId, carId, driverId), Trip Started (tripId, reservationId, carId), Trip Ended (tripId, km), Car Cleaned (carId), Driver Registered (driverId), Driver License Verified (driverId), Driver Signed In At App (driverId).

The current design has one stream "Fleet Activity" that receives every event above.

Define the streams and their identities.
