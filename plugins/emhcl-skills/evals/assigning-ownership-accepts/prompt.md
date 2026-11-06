---
description: Owner teams and team links for a bike rental.
tags: [method, delivery]
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
---

Give each element of our bike rental model one owner team, and show how the teams depend on each other. Do not write files. Answer in the reply.

Teams: Rental (rides), Billing (charges), Fleet (bikes). The teams want high autonomy. A card provider outside our company charges the card.

The model:
- A rider starts a ride on the Start Ride screen. The command Start Ride records Ride Started. Start Ride refuses a bike that is out of service.
- A rider ends a ride on the End Ride screen. The command End Ride records Ride Ended.
- The read model Active Rides builds from Ride Started and Ride Ended and feeds the rider app.
- The automation Ride Charger reads its todo list Rides To Charge (built from Ride Ended and Ride Charged) and issues Charge Ride. Charge Ride records Ride Charged. The charge goes through the card provider.
- A mechanic reports damage with Report Damage, which records Damage Reported.
- The fleet manager blocks a bike with Block Bike, which records Bike Blocked.
- The automation Bike Blocker reacts to Bike Blocked and issues Take Bike Out Of Service, which records Bike Taken Out Of Service.
