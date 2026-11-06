---
name: eventmodeling-planning-slices
description: Lists the delivery slices of an event model and writes the delivery status of each slice. For each slice, it reports the events that the slice uses and produces, its upstream and downstream slices, and its contract (precondition and postcondition). Use it when someone asks to plan the build, to list the slices and their dependencies, to see what a team can build in parallel, or to mark slices as planned, blocked, in progress, or done. Writes slice status only. Does not write events, commands, read models, automations, or ownership, and does not estimate delivery time.
metadata:
  version: "1.0.0"
  contract: "K0 K3 K8 K9 H0 H3 H11"
---

# Planning slices

This skill makes the slices of a model visible for the build and gives each slice a delivery status. Each slice has one primary element of the kinds in K3. For each slice, the skill reports the events that it uses and produces, its neighbors, and its contract, so that teams can build slices in parallel. It writes the slice status part and no other part.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read these parts as input: events, commands, read models, automations, lifecycles, command scenarios, read model scenarios, ownership when it exists, and the records on them.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`. In HCL, each workflow is one slice (H3, H11), so the slices exist before this skill starts.

Slice status comes after the reviews. If a review finding is still open, give the slice report, report the open finding, and write a status only when the person asks for it.

## Procedure

1. Resolve each open request on your part first. A request that asks for a status change gets that status, or a decision (K8) that states why the status stays.
2. List each command, read model, and automation. Count an element that is used in two places once.
3. Find the slice of each element. In an `.em.hcl` model, the slice is the workflow that holds the element.
4. If an element has no slice, or one slice holds more than one element, do not fix it. Write a request (K8) on the element, concerning the part of that element: commands, read models, or automations.
5. Give each slice its kind and its name under K3.
6. List the events that each slice uses and produces:
   1. State change: it uses the events that its command decides from. These are the earlier events of its stream that lead to the states before its move in the lifecycle, and the given events of its scenarios. It produces the success events of its command.
   2. State view: it uses the events that build its read model. It produces no event.
   3. Automation: it uses the events that start it and the events that open and close its todo list. It produces the events of the command that it issues.
7. Find the dependencies. Slice B is downstream of slice A when B uses an event that A produces. Name that event for each dependency.
8. Name the pattern of each dependency. Use the dependency patterns below.
9. Write the contract of each slice. Use the contract section below.
10. Decide the status of each slice. Use the status table below.
11. Write the status of each slice. In an `.em.hcl` model, write `status` on the workflow (H11). Never change a status that H0 protects unless the person asks for it.
12. Report the slices with the slice template below.

## Dependency patterns

Most dependencies follow one of three patterns:

1. Command to event to command. Slice A produces an event. The command of slice B decides from that event. Each slice keeps its own state.
2. Command to event to read model. Slice A produces an event. The read model of slice B shows data from that event. This is the most frequent pattern.
3. Command to event to automation. Slice A produces an event. The automation of slice B reacts to it.

A slice that uses an event from another slice is downstream of that slice. Two slices that share no event have no dependency.

## Contract of a slice

A contract is the promise that a slice makes to the slices after it. It lets a team start before the upstream slice is finished.

- Precondition: what must be true before the slice runs. Usually this is an event of an upstream slice, or a state of the stream.
- Postcondition: the events that exist after the slice runs, and the fields that they carry.

A downstream team builds against the postcondition of the upstream slice. In its tests, it uses a sample of the upstream event.

## Status table

| Status | When to write it |
| --- | --- |
| created | The element exists, but its scenarios or its reviews are not complete. |
| planned | The element is complete, the gates before slice status pass, and no open record is on the slice. |
| assigned | The slice is planned and the ownership part names its owner team. |
| blocked | An open question or an open request is on the slice or on an event that it uses. |
| in progress, review, done | Only when the person states it, or an evidence source of the kind code shows it. |
| informational | The person agrees that the team will not build the slice, for example a step of another system. |

In an `.em.hcl` model, write `in_progress` for "in progress".

## Rules

1. Add no event, command, read model, automation, field, or scenario. Change no element of another part (K0).
2. Write no owner team and no time estimate.
3. Each dependency names one event. Never record a dependency through a call or through shared state (K3).
4. A status change touches only the slice that it names.
5. Use the business names of the elements in the report. Put model labels only where the person reads the model file.

## Slice template

Report each slice with these parts:

- Slice: the name of the element.
- Kind: state change, state view, or automation.
- Element: the command, read model, or automation, with one sentence about what it does or shows.
- Events used: each event that the slice reads, and why.
- Events produced: each event that the slice writes, and when.
- Upstream: each slice that produces an event that this slice uses.
- Downstream: each slice that uses an event that this slice produces.
- Precondition and postcondition: the contract of the slice.
- Status: the status that you wrote, and for a blocked slice, the open record that blocks it.

Read `references/examples.md` when you need a worked slice list with dependencies.

## Result

This skill writes the slice status part: one status for each slice. It also writes requests for elements that break K3, and decisions for status changes that it declines.

It reports to the person the slice list in the template, the dependencies with their events and patterns, each status change, and each request that it wrote.

## Done when

1. The report lists each command, read model, and automation in exactly one slice, or it names the request that the skill wrote about that element.
2. Each slice in the report states its kind, its events used, its events produced, its upstream slices, its downstream slices, its precondition, and its postcondition.
3. Each dependency in the report names the event that links the two slices.
4. Each slice has a status in the model, and the report names the open record of each blocked slice.
5. No open request on slice status remains.
6. The skill changed no part other than slice status, apart from the requests and decisions that it wrote.
7. In an `.em.hcl` model, `emhcl validate --profile workshop` shows no core error that the change caused.
