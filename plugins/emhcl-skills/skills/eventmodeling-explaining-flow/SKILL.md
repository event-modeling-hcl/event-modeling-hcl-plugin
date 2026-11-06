---
name: eventmodeling-explaining-flow
description: Explains one flow that the model already holds, one step for each slice in the order the slices run. Each step says what the person sees and does, what the system records, and what becomes visible or starts next, with the rules from its scenarios. Use it when someone asks how an existing flow works, for example "how does renting a bike work?" or "walk me through checkout". Does not assess a new, planned, or missing feature, and does not follow one single value through the model. Writes nothing.
metadata:
  version: "1.0.0"
  contract: "K0 K3 K9 H0 H3 H9"
---

# Explaining a modeled flow

This skill turns a modeled flow into a short guided explanation. A flow is the chain of slices that one feature runs through. The person gets a summary of 1 to 3 sentences and one step for each slice, in run order. The skill writes nothing. Every statement comes from the model, and every gap is an open question in the reply.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

You read these parts of the model:

- The chapters, their slices, and the elements of each slice.
- The chapter summary, if the chapter has one. It gives the purpose of the chapter and the decisions behind it.
- The fields and the scenarios of the slices that you choose.

The flow must exist in the model. If the person names something new, planned, "support for X", or not in the model, explain only the parts that exist and tell the person that the rest is a planned change. Do not sketch new slices.

If the model is an `.em.hcl` file or folder, a slice is one workflow and the board gives the run order (H3). Scenarios follow H9.

## Procedure

### Choose the subject

1. Take the subject from the message of the person. If the person points at a part of the model with "this" or "here", use that part.
2. If the model is empty, tell the person that there is nothing to explain yet.
3. If no subject is given, or several chapters fit equally well, ask before you read the model in detail (K9). Offer the chapters as options, or the main slices when the model has one chapter. List first the flow that the person looks at now.

### Find the slices

4. Find the chapter or the chapters of the subject by their names, and read their summaries.
5. Make an outline of the slices in these chapters, with element names only.
6. Find the slice where the flow starts and follow the connections to the slice where it ends. Use the usual path: screen, command, event, read model, next screen (K3).
7. Also follow each event into the automations that it feeds.
8. Go into another chapter only through an event from another system.
9. Stop when a further slice adds nothing that the person asked about.
10. If the flow has more than 20 slices, tell the person that the subject is several features. Explain the first feature only, and name the others.

### Read the chosen slices

11. Read the fields, the connections, and the scenarios of each chosen slice. Do not read the rest of the model in detail.
12. A scenario title in business words is a rule. Its given, when, and then say when the rule applies.

### Build the steps

13. Make one step for each slice, in run order. Never split a slice into one step for each element. Never make a step for a scenario.
14. Tell each step as the person lives it: what they see and do, what the system records, and what the step makes visible or triggers.
15. For an automation slice, say what the automation picks up, which action it starts, and what the system records.
16. Give each step the parts in the table below.
17. Write the summary in 1 to 3 sentences about how the flow works. Do not put the slice count into the summary.

| Part | Content |
| --- | --- |
| Title | The name of the slice as the model writes it. |
| Description | 1 to 3 sentences about what happens in the slice and why it matters. Use the language of the model. Use no identifiers. |
| Screen | Only when the person sees a screen that is not part of the slice. |
| Rules | The business rules of the slice, one line each, from its scenarios only. Copy each threshold exactly. Write "none" when the slice has no scenario. |

### Report the gaps

18. If no scenario states a rule, the rule does not exist in the model. Do not state it as a rule.
19. If the flow shows a gap, write it into the description of that step as an open question.
20. If the person wants the gap recorded in the model, tell the person that it needs an open question record on that element.

Read `references/examples.md` when you need a full example of the result.

## Rules

1. One step is one slice. A step never shows one element alone.
2. The rules of a step come only from the scenarios of its slice.
3. Each fact comes from the model. General domain knowledge never becomes a step or a rule.

## Result

The skill writes nothing in the model.

It reports a numbered list. The list starts with one line that names the flow and the number of slices. The summary follows. Then comes one numbered item for each step, with its title, description, and rules.

## Done when

1. Each step is one slice, and the steps follow the run order of the model.
2. Each rule comes from a scenario of its slice, and each threshold matches the model exactly.
3. The subject is a flow that the model holds, or the person chose it after a question.
4. Each step says what the person sees and does, what the system records, and what becomes visible or triggered.
5. Each gap is an open question in the step, not a rule.
6. A flow over 20 slices is split, and only the first feature is explained.
7. The summary has from 1 to 3 sentences.
8. The model is unchanged.
