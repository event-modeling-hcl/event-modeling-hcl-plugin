---
name: eventmodeling-assigning-ownership
description: Gives each event, command, read model, and automation of an event model one owner team, following Conway's law, and reports the team boundaries, the events that cross them, the external systems and their owners, and each cycle between teams. Use it when someone asks which team owns what, how to split the work between teams or systems, who owns an integration with another system, or where teams depend on each other. Writes ownership only. Does not write roles or teams, events, automations, or slice status.
metadata:
  version: "1.0.0"
  contract: "K0 K3 K8 K9 H0 H11"
---

# Assigning ownership

A system mirrors the structure of the teams that build it (Conway's law). This skill uses that law to give each element of the model one owner team, so that each team can build and deploy its part with little coordination. A team and a system name the same boundary. The skill writes the ownership part.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read these parts as input: roles (the teams and the external systems), events, streams, lifecycles, commands, automations, read models, screens, slice status, and the records on them.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`. There, the owner goes on each workflow and on each internal context of events (H11).

If the person says that teams do not matter, the ownership part needs no owner. Report that and write nothing.

## Questions about the teams

Ask these questions under K9, and only when no source answers them:

1. How are the teams organized: one team for all, teams by business domain, or teams by technical function?
2. If the teams follow business domains, what does each team own?
3. If the teams follow technical functions, offer a split by business domain as an option.
4. How much autonomy does each team need: high, moderate, or low? High autonomy means that teams talk only through events. For low autonomy, ask why the teams accept the coupling.
5. Which external systems does the process use, such as a payment provider or a carrier? Which team owns each integration: an existing team or a new team?

## Procedure

1. Resolve each open request on your part first.
2. If a team that the person names is not in the roles part, write a request (K8) concerning roles. Give elements to that team only after it exists.
3. Find the system boundaries. For each system, name what it owns, the events that it produces, and the streams and lifecycles that it controls. One stream belongs to one system.
4. Give each event one owner team: the team of the system that writes the event. In an `.em.hcl` model, the owner of an event is the owner of its context. If one context holds events of two teams, write a request (K8) on one of those events, concerning events.
5. Give each command the owner team of the events that it produces. If its events belong to two teams, write a request (K8) on the command, concerning commands.
6. Give each read model to the team that maintains the screen or the automation that reads it.
7. Give each automation a home team. Use the automation section below.
8. Give the translation step of each event from another system to the team that owns that integration. If such an event reaches an internal element with no translation step, write a request (K8) on that element, concerning automations.
9. Find the links between teams. For each pair of teams, name the triggering event, the reacting command, automation, or read model, and the resulting event.
10. If a team uses the state of another team in a way other than an event, write a request (K8) on that element, concerning its part.
11. Look for cycles between teams. A cycle exists when team A uses an event of team B, and team B uses an event of team A, directly or through other teams. Report each cycle to the person. Do not break it here.
12. Write the owner of each element. In an `.em.hcl` model, write `owner` on each workflow and on each internal context (H11).
13. Write the report. Use the report sections below.

## Automations and their home team

For each automation, state these facts:

- what starts it,
- what it decides,
- which command it issues, or that it issues none,
- which team owns it.

An automation lives with the team that owns the command that it issues. An automation that only informs people lives with the team that runs it.

## Rules

1. Each element has exactly one owner team. Never split one element between two teams.
2. Teams link only through events (K3). No team reads or changes the state of another team.
3. Do not add a system for each team name when the model has no such boundary.
4. Do not redesign a translation step or a chain of automations. Write a request (K8) instead.
5. An external system keeps its own events. Its integration has one internal owner team.

## Report sections

1. System boundaries. One entry for each system: owner team, responsibilities, commands, events produced, events used, read models, dependencies, and stream identity.
2. Event flow across boundaries. The events in time order, with the team that each event moves the work to.
3. Team responsibility matrix. One line for each team with its commands, events, and read models.
4. Communication between teams. One entry for each pair: triggering event, reaction, and resulting event.
5. External systems. Name, owner team, the internal system that talks to it, and purpose.
6. Independent work. How the boundaries let each team build, test, and deploy alone, and each cycle that prevents it.

Read `references/examples.md` when you need a worked report.

## Result

This skill writes the ownership part: one owner team for each element. It also writes requests for changes in other parts. It reports the six report sections to the person, with each request that it wrote and each cycle that it found.

## Done when

1. Each event, command, read model, and automation has one owner team in the model, or the report states that teams do not matter to the person.
2. Each link between two teams in the report names the event that carries it.
3. Each automation has a home team in the report.
4. Each external system has an internal owner team for its integration.
5. The report names each cycle between teams, or states that no cycle exists.
6. No open request on ownership remains.
7. In an `.em.hcl` model, `emhcl validate --profile workshop` shows no core error that the change caused.
