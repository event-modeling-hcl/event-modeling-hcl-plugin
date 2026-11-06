# Worked example: a remote workshop for a kayak rental

A kayak rental wants a model of booking and return. The model already holds roles and events. The first gate that fails is chapters. The group meets remotely on two mornings.

## Session plan

Participants:

| Person | Role |
| --- | --- |
| Ana | Product owner (required) |
| Ben, Chloe | Developers (required, two) |
| Dev | Tester (required) |
| Eva | Facilitator (required) |
| Finn | Rental desk employee (optional, real user) |

Each required role is present.

Morning 1, 90 minutes:

| Time | Part | Time box |
| --- | --- | --- |
| 09:00 | Goal of the session and first failing gate | 5 minutes |
| 09:05 | chapters and story order (two chapters: Booking, Return) | 25 minutes |
| 09:30 | Break | 10 minutes |
| 09:40 | screens (four screens) | 25 minutes |
| 10:05 | Break | 10 minutes |
| 10:15 | streams | 10 minutes |

Morning 2, 90 minutes:

| Time | Part | Time box |
| --- | --- | --- |
| 09:00 | lifecycles (two streams) | 20 minutes |
| 09:20 | Break | 10 minutes |
| 09:30 | commands | 20 minutes |
| 09:50 | Break | 10 minutes |
| 10:00 | read models | 15 minutes |
| 10:15 | Open questions and next steps | 15 minutes |

The rental has no automation and no event from another system, so the automations gate and the external mappings gate pass at once. The plan stops at read models. Command scenarios start the next session.

## Follow-up summary

Participants: Ana (product owner), Ben and Chloe (developers), Dev (tester), Eva (facilitator), Finn (rental desk employee).

Decisions:

1. A booking holds one kayak. Reason: Ana states that groups book each kayak on its own.
2. The return screen shows the booking of the kayak at the desk. Reason: Finn scans the kayak, not the customer card.

Open questions:

1. Does a customer pay a fee for a late return? On the command Return Kayak.
2. Who can cancel a booking on the day of the rental? On the command Cancel Booking.

First failing gate: command scenarios. The next session starts there.

Next steps:

| Step | Person | Date |
| --- | --- | --- |
| Answer the late fee question | Ana | Friday |
| Send the rental desk process on paper | Finn | Friday |
| Plan the next session | Eva | Monday |

Please send corrections and missed items by Friday.
