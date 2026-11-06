---
name: eventmodeling-plotting-timeline
description: Puts the steps of one chapter in causal order and writes, for each step, what comes before it, what triggers it, what must be true first, and the end state of each path. Use it when someone asks to order the events of a journey, lay out a timeline, find what triggers a step, or find where each path of a process ends. Writes story order only. Does not create or split chapters, and does not write commands or lifecycles.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K3 K7 K8 K9 H0 H3 H10"
---

# Plotting the timeline of a chapter

This skill tells the story of one chapter in time order. It writes the story order part (K0): the order of the steps, the trigger and precondition of each step, and the end state of each path.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- One chapter of the chapters part, and its events.
- The roles part.
- The lifecycle states, when they exist.
- The open requests on the story order part.

If the model has more than one chapter and the person named none, follow K9 to choose one. Work on that chapter only.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`. In an `.em.hcl` model the story order is the `board` (H3). Write it only when the slices exist. Until then, report the timeline to the person and leave the story order gate open.

## Procedure

1. Resolve each open request on your part first.
2. Take the steps of the chosen chapter only.
3. Find the step that starts the story.
4. For each next step, find what must happen before it. That step is its predecessor.
5. Put each step after its predecessor. The story reads forward (K3).
6. For each step, write its trigger: the role, the system actor, or the time that makes it happen.
7. For each step, write its precondition in plain words, for example "the bike is free".
8. Find each place where one trigger ends in more than one result. Each is a decision point.
9. Show each decision point as sibling paths after the same step, for example "card charged" or "charge failed".
10. If a branch has different screens and commands because it begins another journey, leave it out of this timeline. Write a request (K8) concerning the chapters part, on the first element of the branch.
11. Follow each path until it ends. Name the end state of each path, for example "ride paid" or "reservation expired".
12. For each failure path, find what the business does to undo earlier steps. If an undo event is missing, write a request (K8) concerning `event`.
13. Place an event from another system as one handover at the moment it drives this story. Continue with this chapter's own steps after it.
14. If a long run of steps belongs to another system, follow K9 to decide whether it is its own chapter.
15. Make sure that each step of the chapter has a place in the order.
16. Follow K9 for each unclear order or cause, and record it as an open question (K8).
17. In an `.em.hcl` model, write the trigger and precondition into the `description` of the workflow of the step, or name the lifecycle state. If an end state has no lifecycle state, write a request concerning `lifecycle`.

Read `references/examples.md` when you need a worked timeline with branches and undo events.

## Rules

1. One run plots one chapter. Never move a step to another chapter.
2. Each step has a predecessor, except the first step of a path.
3. A step with no trigger is a gap.
4. Each branch is a decision point inside this chapter.
5. A path that stops in the middle is a gap. A failure path ends in an end state or in its undo steps.
6. An event from another system is a single handover, not a part of this story.

## Result

The skill writes the story order part of one chapter: the order of its steps, the trigger and precondition of each step, the paths, and their end states. In an `.em.hcl` model that is the order of `board.workflows` and the workflow descriptions. It writes open questions and requests (K8).

Report to the person: the timeline, its main path, its decision points, its end states, and each request.

## Done when

1. Each step of the chapter has a place in the order.
2. Each path reaches a named end state.
3. Each step has a predecessor or starts a path, and has a trigger and a precondition.
4. Each branch is a decision point, or a request on the chapters part names it.
5. Each failure path has its undo steps, a request for them, or a decision that no undo exists.
6. Each event from another system is a single handover.
7. No open request on the story order part remains.
