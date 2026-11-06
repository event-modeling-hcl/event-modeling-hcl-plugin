---
name: eventmodeling-deriving-commands
description: Derives one command for each screen action and each trigger inside the system, such as a timer, with one issuer, one role, typed fields, business rules, preconditions from the lifecycle, a success event, and named failures. Use it when someone asks what actions a user or the system can take, asks to turn the buttons of a screen into commands, or asks which inputs and preconditions an action needs. Does not write screens, events, read models, automations, or scenarios.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K2 K3 K6 K7 K8 K9 H0 H3 H5 H6 H10"
---


# Deriving commands

This skill gives the model its commands. Each screen action and each trigger inside the system gets one command. Each command carries every value that its rules read, or reads the value from earlier events of its stream. The skill writes the commands part only.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read these parts of the model:

- roles: human roles and system actors
- screens: their fields and the action that each one offers
- automations: the processors that issue commands
- events and streams: the facts and the stream identity of each event
- lifecycles: the states, the moves, and the refused moves

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

If you do not know which actions a person starts and which the system starts, ask that first (K9).

## Procedure

1. Resolve each open request on your part first.
2. List each action on each screen. Each action becomes one command.
3. List the triggers and processor actions inside the system, including translation steps and timers. Each processor action becomes one command in that automation's slice (K3).
4. Do not invent a command to cause a foreign event. Derive the translation command from its processor. If that processor is missing, request the automations part.
5. Name each command in the imperative with business words (K1).
6. Give each command one issuer (a screen or an automation) and one specific role or system actor.
7. List the typed fields of each command. Add only fields that the command needs. Give each field an origin under K2.
8. Write each business rule that the command enforces on its fields.
9. Read the lifecycle. Write each precondition from the state of the stream (K7).
10. For each rule and each precondition, list every value that it reads. Make sure that each value is a command field or comes from earlier events of the stream.
11. Add each context value that a rule reads as a generated command field (K2).
12. Name the success event. If it does not exist, write a request (K8) on the command, concerning events.
13. Name each failure, and say whether it is a rejection with no event or an event that the business records (K1).
14. If a field depends on another field, write the condition. Example: a card number only when the payment method is card.
15. If a screen field that the command needs does not exist, write a request on the screen, concerning screens.
16. If a lifecycle move or refused move for the command is missing, write a request on the lifecycle, concerning lifecycles.
17. Apply the multi-stream boundary test of K1. If the command needs a different boundary, request the streams part instead of inventing a cross-stream atomic action.

## Rules

1. One command for each screen action and each processor action, including a translation action. A timer needs the business fact that opens its work.
2. A conditional field names the field that it depends on and the value that turns it on.
3. Preserve a deliberately omitted issuer only under K1 and its notation binding. Never use that exception for an unexplained trigger.
4. In an `.em.hcl` model, a person's command belongs to its screen's `state_change`. A processor's command belongs to its `automation`. If the automation is missing, request it instead of creating an unrelated state change.

## Result

This skill writes commands, their fields, their rules, and their success and failure outcomes, plus their records (K8). It reports to the person:

| Item | Content |
| --- | --- |
| Command | Name, issuer, role |
| Fields | Name, type, origin, condition of a conditional field |
| Rules | Each business rule and the values that it reads |
| Preconditions | Each required state of the stream |
| Outcomes | The success event and each named failure |
| Requests | Each request written on another part |

Read `references/examples.md` for worked commands with context fields and conditional fields.

## Done when

1. Each screen action and processor action has exactly one command. Foreign events retain their outside cause and have translation commands only for the receiving domain's facts.
2. Each command has one issuer and one specific role or system actor.
3. Each command field has a type and an origin under K2.
4. Each value that a rule or precondition reads is a command field or comes from earlier events of the stream.
5. Each context value is a generated command field.
6. Each precondition matches a state of the lifecycle, or a request on the lifecycle exists.
7. Each command names one success event and its failures.
8. Each conditional field states its condition.
9. Each open request on the commands part is resolved.
