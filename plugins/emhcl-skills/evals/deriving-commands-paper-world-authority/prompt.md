---
description: Command decisions use authoritative stream facts despite a stale display and preserve automatic expiry.
tags: [method, structure, paper-world]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Derive only the commands for the following equipment-hire model. All inputs are inline; do not look for fixture files. Give the command contracts and the outcome of the concrete collection attempt in the reply. Do not write files or rewrite the other model parts.

Existing model parts:
- Roles: Member (human) and Reservation Expirer (system actor).
- Stream: Equipment Unit, identity unit_id (text). Events carry reservation_id (text) to distinguish successive reservations of the same unit.
- Events: Unit Reserved (unit_id, reservation_id, member_id, expires_at); Reservation Cancelled (unit_id, reservation_id); Unit Collected (unit_id, reservation_id, member_id, collected_at); Reservation Expired (unit_id, reservation_id, expired_at). Times are UTC timestamps and IDs are text.
- Lifecycle: Available becomes Reserved on Unit Reserved. Cancellation or expiry takes Reserved back to Available. Collection takes Reserved to Collected. No collection is allowed from Available or Collected.
- Screen "Collect Equipment" belongs to Member and has one action, "Collect". It submits unit_id and reservation_id selected from the Member's Reservations view. That view also shows member_id, reservation status, and expires_at. It can lag behind the recorded events.
- The existing reservation-expiry automation belongs to Reservation Expirer. It reads an Expiring Reservations todo list containing unit_id, reservation_id, and expires_at and runs when the deadline is reached. No member or clerk starts it.
- Collection rule: only the authenticated member who owns the active reservation may collect, and only before its expiry time. A refusal records no business event.
- Expiry rule: at or after the deadline, expire the matching reservation only if it is still active. Do not expire a cancelled or collected reservation. A skipped or refused expiry records no business event.

Concrete attempt:
- At 09:55 the Member's Reservations display says unit U-7 is reserved under R-12 for member M-8 until 10:05.
- The authoritative Equipment Unit stream then records Reservation Cancelled for U-7 / R-12 at 09:58. This is the latest event in the stream.
- Authenticated member M-8 presses Collect for U-7 / R-12 at 10:00 while the display still says Reserved.

Give each command one issuer and actor, its typed inputs and their origins, rules/preconditions, and success/refusal outcomes. Address the stale display in the collection outcome without adding a new business rule.
