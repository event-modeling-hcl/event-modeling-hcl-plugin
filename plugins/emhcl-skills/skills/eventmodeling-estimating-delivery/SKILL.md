---
name: eventmodeling-estimating-delivery
description: Estimates the delivery time of an event model from its slices, a weight for each slice, the event dependencies between slices, and the measured velocity of the teams. It groups the slices into dependency phases, gives the time of each phase and the total, and shows how the time changes with more capacity. Use it when someone asks how long the build takes, for a delivery plan, a forecast, or a sprint count, or what one more developer changes. Writes nothing in the model. Does not write slice status or ownership.
metadata:
  version: "1.0.0"
  contract: "K0 K3 K9 H0 H11"
---

# Estimating delivery

This skill turns the slices of a model into a delivery estimate. It weights each slice, groups the slices into dependency phases, and divides the size of each phase by the velocity of its teams. Velocity is the weighted number of slices that a team finishes in one sprint. The skill writes nothing in the model.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read these parts as input: slice status, ownership, commands, read models, automations, command scenarios, read model scenarios, and the events that link the slices. If the person gives a slice report with dependencies, use it. Otherwise find the dependencies under K3: a slice depends on another slice only through an event that the other slice produces.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`. Each workflow is one slice, with its status and its owner (H11).

You need the measured velocity of each team. If no history exists, ask the person for a first value under K9. In autonomous mode, take a value and label it as assumed.

## Weights

Give each slice one weight.

| Weight | Typical slice | Value |
| --- | --- | --- |
| Simple | A read model with few fields | 0.5 |
| Typical | A command with a few business rules | 1 |
| Complex | A command or an automation with many rules, or with an external system | 2 |

Base each weight on the scenarios of the slice. Many scenarios, external failure cases, or an external system give a higher weight.

## Procedure

1. List the slices that remain. Leave out each slice with the status done or informational. Count a slice in progress or in review with its full weight, unless the person gives the part that is left.
2. For each slice, list its kind, its owner team, and its upstream slices.
3. Give each slice a weight from the table.
4. Add the weights. The sum is the size of the work.
5. Get the velocity of each team in weighted slices per sprint, with its source.
6. Group the slices into dependency phases. Use the phase section below.
7. Give each phase to the teams that own its slices. Without ownership, use one team.
8. For each phase, divide the weight of each team by the velocity of that team. The longest result is the time of the phase.
9. Add the times of the phases. The sum is the delivery time of the slices.
10. Ask for the time budget of work outside slices, such as meetings, planning, documents, and deployment. Add it as its own line.
11. Show the capacity options. Use the capacity section below.
12. Write the plan. Use the result section below.

## Dependency phases

A phase is a set of slices that can run at the same time.

1. Put each slice with no upstream slice into the first phase.
2. Put a slice into the next phase when all its upstream slices are in earlier phases.
3. A slice can join the phase of an upstream slice when it needs only the postcondition of that slice: the event and its fields. A state view slice often depends this way (K3). Its team uses a sample of the upstream event in its tests. Mark that dependency as "contract only" in the plan.
4. Slices that share no event with the other slices form an independent track that runs beside the phases.

## Capacity

Show the person how the time changes with more capacity. Examples are one more developer, better tests, or a faster delivery pipeline. For each option, divide the same size by the new velocity. Label each new velocity as assumed until a sprint measures it.

## Rules

1. Weight slices, never features. A feature with several slices gets the weight of each slice.
2. A plan that runs every slice in parallel is wrong. The phases follow the event dependencies.
3. Work outside slices is never a slice. It gets its own time budget.
4. Each velocity has a source: measured sprints, or a value labeled as assumed.
5. Copy each number that the person gives exactly. Keep two decimals in each step. Round only the total, and state the rounding.
6. Change nothing in the model.

Read `references/examples.md` when you need a worked estimate.

## Result

This skill writes nothing in the model. It gives the person a plan with these parts:

- the slice list with kind, owner team, upstream slices, and weight,
- the phases with their slices and teams, and each contract-only dependency,
- the velocity of each team and its source,
- the time of each phase, the time outside slices, and the total,
- the capacity options,
- the assumptions.

## Done when

1. Each remaining slice has exactly one weight in the plan.
2. No slice is in an earlier phase than one of its upstream slices, except a dependency that the plan marks as contract only.
3. Each velocity in the plan has a source: measured sprints or a value labeled as assumed.
4. Work outside slices has its own time budget in the plan.
5. The plan gives the time of each phase and the total.
6. The plan lists each assumption.
7. The model is unchanged.
