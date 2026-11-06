---
name: eventmodeling-brainstorming-events
description: Collects the business events of a domain as past-tense facts, each with the identity of its thing and one or two key facts. Use it when someone asks what happens in a domain, asks to list or brainstorm the events, asks which facts the business keeps, or wants to clean up a list of events. Writes events only. Does not write roles, chapters, story order, streams, commands, or read models.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K2 K6 K8 K9 H0 H2 H10"
---

# Brainstorming business events

This skill finds what happens in the domain. It writes the events part (K0): each business event and the facts that it carries. Each event holds the identity of the thing it is about and the one or two facts that make it useful.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- The roles part of the model.
- The sources: requirements, notes, documents, answers from people.
- The events part of the model, if it exists. Look only for what is missing.
- The open requests on the events part.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

## Procedure

1. Resolve each open request on your part first.
2. Name the main things whose story the domain tells, for example a rental, a bike, a payment.
3. For each thing, name the value that tells one instance from another. This is its identity.

   If the work is unclear, use the offline-first reset in K1 before listing its events. Walk one real case. Ask:
   - What arrives, and who receives it?
   - Which sheet or prior fact does the actor read?
   - What does the actor decide and record?
   - Who receives the result, and what starts their next action?

   Ask about a correction, a missing fact, a delay, and a disputed decision. Use the answers as evidence or questions on your part. Send requests for changes to other parts under K0.

4. Walk the work of each role and each system actor. List the steps they take and where they choose.
5. For each step, ask "did something change that the business keeps?" If yes, write an event.
6. Capture events fast first. Remove the weak ones after the list stops growing.
7. Name each event under K1.
8. Give each event its identity field and the one or two facts that make it meaningful. Use business names for facts, "riderId", not "userId".
9. Give each fact an origin under K2. Only an identifier that the system makes when it records the fact starts on the event.
10. If an event means only "this happened", keep only its identity field.
11. Make sure that a role or a system actor of the roles part causes each event. If none does, write a request (K8) concerning the roles part.
12. List the business rules that the sources state, with their condition and their result.
13. For each rule, find whether the business keeps a record when the rule stops an action. Follow K9 when no source tells it.
14. If the business keeps that record, add a failure event under K1, for example "Ride Start Refused" with the reason.
15. If the business keeps no record, add no event. Name the rule in your report.
16. Find what happens when a payment fails, a thing breaks, or time runs out. Add the events that the business records.
17. Remove each event that only names a record change, such as "Rental Updated". Find the business moment under it.
18. Merge two events that mean the same thing. Keep the business name, and record the merge as a decision (K8).
19. Give each event an evidence record under K8.

Read `references/examples.md` when you need a worked list with weak events removed.

## Rules

1. An event is a business moment, never a create, update, or delete of a record.
2. Two events never mean the same thing.
3. Start with few facts. A part that needs more facts later writes a request (K8) concerning `event`.
4. An event refers to no command, chapter, or position in the story. Those belong to other parts.

## Result

The skill writes the events part: each event with its name, its identity field, and its key facts. In an `.em.hcl` model it can also write the `field_type` blocks of recurring concepts (H2). It writes evidence, open questions, assumptions, and decisions on these events (K8).

Report to the person: the event list with key facts, the events that you removed or merged and why, and the business rules that the sources state. Each rule without a failure event becomes a refused command later.

## Done when

1. Each event has a past-tense name in business words.
2. Each event carries its business identity and captured facts. Changing calculations stay in read models. A decision-time value follows K1 until the business decides it.
3. No event is a create, update, or delete of a record.
4. No two events mean the same thing.
5. Each known error and limit is a failure event or a rule in the report.
6. A role or system actor of the roles part causes each event, or a request on the roles part names the gap.
7. Each event has an evidence record with a certainty.
8. No open request on the events part remains.
