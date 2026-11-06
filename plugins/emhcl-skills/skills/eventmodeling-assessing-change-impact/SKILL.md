---
name: eventmodeling-assessing-change-impact
description: Shows what a planned change needs from the model, one step for each slice in flow order, each marked as existing, changed, or new. A new slice appears as a proposal with its kind, its fields, and a plain description of its screen. Use it when someone asks what a new feature, field, or rule changes, for example "we want a deposit for day rentals, what does that touch?", or when a flow is planned but not in the model yet. Does not explain a flow that is already complete, and does not apply the changes. Writes nothing.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K2 K3 K6 K9 H0 H3 H9"
---

# Assessing the impact of a planned change

This skill shows what a planned change needs from the model before anyone builds it. The person gets each slice that the change uses or needs, in the order the flow runs. Each slice is existing, changed, or new. A new slice is a proposal, not a decision. The skill writes nothing.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

You read these inputs:

- The change, in the words of the person: a new feature, field, rule, or a flow that the model does not have yet.
- The chapters, slices, elements, fields, and scenarios of the model.
- The chapter summary, if the chapter has one.
- Open requests on the elements, when the person asks for a view of proposals that are still open.

If the model is an `.em.hcl` file or folder, a slice is one workflow and the board gives the flow order (H3). Scenarios follow H9.

## Procedure

### Understand the change

1. Take the change from the message of the person. If the person points at a part of the model with "this", use that part.
2. If the person names no change, or the change fits several chapters equally well, ask (K9). Do not guess.
3. If the flow is complete and the person asks only how it works, show each slice as existing and add no proposal.

### Find where the change lands

4. Find the slice where the change lands first: the slice where new data enters, or the slice whose event changes its meaning.
5. Search the names of elements and fields for the concept of the change, with its obvious variants and short forms. Treat each slice that already mentions it as a candidate.
6. Trace downstream from the first slice. Include each slice whose events carry the change, each state view and automation that these events feed, and each screen that shows the changed information.
7. Trace upstream to the place where the needed data comes from (K2).
8. Work out the slices that the change needs and the model does not have. Each new command, new read model, or new automation is one new slice (K3).
9. Stop widening the trace when a further slice adds nothing new about the change.
10. If the change needs more than 20 slices, tell the person that it is several changes. Assess the first one, and name the others.

### Read the chosen slices

11. Read the fields, the connections, and the scenarios of each chosen existing slice. Do not read the rest of the model in detail.

### Mark and describe each slice

12. Give each slice one status: existing (used as it is), changed (needs an adjustment), or new (does not exist).
13. Leave out each unchanged slice that the person does not need to follow the flow. Name an unaffected slice only when the person expects a change there.
14. Put the steps in flow order. Do not group them by status.
15. Give each step the parts in the table below.
16. For a new slice, sketch the elements that its kind holds (K3), with names under K1 and fields with origins under K2. If it reads an existing event, use the name of that event.
17. Describe the screen of a new slice in plain words: a heading and the content, with no navigation. A screen that changes state is a form with one input for each command field and one button named after the command. A screen that shows state is a table with the read model fields as headings and 2 or 3 lines of example data (K6).

| Part | Content |
| --- | --- |
| Title | The existing slice name, or a proposed name that follows the model's naming style. |
| Status | existing, changed, or new. |
| Description | 1 to 3 sentences. For a new slice, start with "Proposed:". |
| Changes | Changed and new slices only. One line for each change, for example "Add the field deposit to Start Rental". |
| Rules | The rules from the scenarios of the slice, one line each, with each threshold copied exactly. Write "none" when there is none. |
| Sketch | New slices only. The elements with their names and fields, and the screen description. |

18. If the change needs a rule that no scenario states, write it as an open question in the step. Do not write it as a rule.

Read `references/examples.md` when you need a full example of the result.

## Rules

1. Each step is one slice, with exactly one status.
2. The steps follow the flow, not the status.
3. Each existing slice comes from the model only. Each new slice and each change is a proposal.
4. Example data on a proposed screen is never a rule.

## Result

The skill writes nothing in the model. The assessment is the proposal.

It reports a numbered list. The first line names the change and the slice count with its split, for example "Deposit for day rentals: 6 slices, 2 exist, 1 changes, 3 are new." A summary of 1 to 3 sentences follows, without the count. Then comes one numbered item for each step. If the person requests implementation, record each change as a request on its element (K0).

## Done when

1. Each needed slice appears once, in flow order, with the status existing, changed, or new.
2. Each changed slice lists its changes one line each, and each new slice starts with "Proposed:" and has a sketch with its kind, fields, and a plain screen description.
3. The trace starts where the change lands and goes downstream and upstream.
4. Each rule comes from a scenario, and each missing rule is an open question.
5. The trace stopped when no further slice added anything new.
6. The model is unchanged.
