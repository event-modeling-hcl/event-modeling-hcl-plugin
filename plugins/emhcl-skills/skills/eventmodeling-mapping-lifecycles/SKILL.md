---
name: eventmodeling-mapping-lifecycles
description: Maps the lifecycle of each event stream: its states, the moves between them with the command and events of each move, the moves that the business refuses with a reason, and the end states. Use it when someone asks for a state machine, the statuses of a thing, which actions are allowed in which state, or where a cancel or failure path ends. Writes lifecycles only. Does not write stream identities, commands, events, or scenarios.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K7 K8 K9 H0 H5 H10"
---

# Mapping stream lifecycles

This skill gives each event stream its lifecycle. It writes the lifecycles part (K0) in the format of K7: the states of one thing, the moves between them, the moves that the business refuses, and the end states. Each cancel, failure, and compensation path reaches an end.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- The streams part and the events of each stream.
- The story order and the screens, when they exist.
- The commands part, when it exists.
- The open requests on the lifecycles part.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`. In an `.em.hcl` model a move names a command. Close the lifecycle in two steps (H3, H5): write the states first, and write the moves and refused moves after the commands exist.

## Procedure

1. Resolve each open request on your part first.
2. Take one stream. Find the event that starts its story. The start move leads to the first state.
3. Name each state that the thing can be in, in business words, such as "Draft", "Booked", or "Closed".
4. Give each state its path and mark each end state (K7).
5. For each event after the first, name the state before it and the state after it.
6. For each move, name the command that causes it. If the command does not exist yet, keep the move in your report with a working name, and write a request (K8) concerning `command`.
7. For each state, list the commands that the business refuses in it, with the reason in business words.
8. Walk the main path from the start move to an end state. Make sure that no event is missing on the way.
9. Walk each cancel, failure, and compensation path. Make sure that each reaches an end state or returns to a named state.
10. If a path starts a new story with its own screens and commands, write a request (K8) concerning the chapters part.
11. If a needed event is missing, write a request (K8) concerning `event`. Do not add the event.
12. Follow K9 for each unclear state or move. Label each assumed state or move as assumed (K8).
13. In an `.em.hcl` model, write one `lifecycle` with its `state` blocks. Write a `transition` or an `invalid_transition` only when its command exists. Leave the gate open while a move waits for its command.

Read `references/examples.md` when you need a worked lifecycle, in a table and in an `.em.hcl` model.

## Rules

1. A state holds no technical flag, such as "isProcessed".
2. A refused move needs a business reason. "Not allowed" is not a reason.
3. A move with no event is a refused move, not a move.

## Result

The skill writes the lifecycles part: one lifecycle for each stream. In the model, or in the reply when the model has no place for it, write two tables for each stream.

| From state | Command | Events | To state | Valid |
| --- | --- | --- | --- | --- |
| (none) | Open booking | Booking opened | Draft | yes |
| Draft | Confirm booking | Booking confirmed | Booked | yes |
| Booked | Return to draft | none | Booked | no: a confirmed booking cannot go back |

| State | End | Path |
| --- | --- | --- |
| Draft | no | main |
| Canceled | yes | cancel |

It writes evidence, assumptions, and requests (K8). Report to the person: the tables, each assumed state or move, each move that waits for its command, and each request.

## Done when

1. Each stream has one lifecycle with exactly one start move and at least one end state.
2. Each refused move names the states, the command, and a business reason.
3. Each state has a business name and a path.
4. The main path reaches an end state with no missing event.
5. Each cancel, failure, and compensation path reaches an end state or a named state.
6. Each move whose command does not exist has a request concerning `command`.
7. Each assumed state or move has an evidence record with certainty "assumed".
8. No open request on the lifecycles part remains.
