---
type: llm
---

PASS if both conditions hold:
1. Each event (Ride Started, Ride Ended, Ride Charged, Damage Reported, Bike Blocked, Bike Taken Out Of Service), each command (Start Ride, End Ride, Charge Ride, Report Damage, Block Bike, Take Bike Out Of Service), each read model (Active Rides, Rides To Charge), and each automation (Ride Charger, Bike Blocker) gets exactly one owner team, and no element is split between two teams.
2. Each link between two teams that the reply names is carried by an event. At least Ride Ended links Rental to Billing, and Bike Blocked links Fleet to Rental.

FAIL if an element has no owner team or two owner teams, or if the reply describes a link between teams as a direct call, a shared table, or a shared state instead of an event.
