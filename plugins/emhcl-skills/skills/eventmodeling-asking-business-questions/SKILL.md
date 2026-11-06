---
name: eventmodeling-asking-business-questions
description: Reads an event model as a fresh business analyst and records plain stakeholder questions about what is unclear or missing, in story order, each with one of eight categories. Also builds the question tour for a prototype or a walkthrough with people who know the business. Use it when someone asks "what is unclear in this model?", "which questions do we ask the product owner?", or "prepare questions for the prototype tour". Does not apply answers, check the model against the modeling rules, or change elements. Writes open question records only.
metadata:
  version: "1.0.0"
  contract: "K0 K4 K5 K8 K9 K11 H0 H10"
---

# Asking business questions about the model

This skill gives a short list of questions that a product owner understands at once. Each question points at something unclear or missing in the model, and it follows the story order. The skill writes records only: one open question with a category (K11) for each question that holds up. Zero questions is a valid result.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

You read these inputs:

- The chapters and the story order of the model.
- The screens, commands, events, read models, and automations, with their fields and connections.
- The scenarios of each slice, and the open questions that already exist in the model.
- For a tour: the prototype or the screens that the people will see, in story order.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

## Procedure

1. Resolve each open request on your part first. Your part is the open questions that this skill wrote earlier.
2. Make a short inventory: each slice and its elements, which slices have scenarios, and the connections.
3. Walk the slices in story order. For each slice, go through the checks below. Skip a check that does not apply.
4. Write a question only if the model gives a concrete reason for it. Name that reason to yourself as evidence.
5. After all slices, look at the shape of the whole model once under K4. Raise a bed directly. Raise the other shapes only after the split tests hold up. Word each one with the stakeholder patterns of K4.
6. For a tour, use the two passes and the order of K11 instead of steps 3 to 5. Give a rule question a setup under K11.
7. Give each question one category of K11 and name its element.
8. Remove each question that the model or an existing record already answers (K9).
9. Write each remaining question as an open question record on its element, with its category and 2 or 3 options when the evidence gives them (K8).
10. Show the person the list in story order.

### What to look for

- rule: Can this step fail? What must be true before the action? In which states must it refuse? Ask "can this fail?" in one open sentence. If an automation or another system depends on a result, ask what happens when it does not answer.
- rule or example: Doing it twice. Ask only when the model gives a reason: a natural key, a scenario that implies uniqueness, a submit with no confirmation, or an automation that can react twice.
- example: Missing examples, from the real fields of the flow. For a flow with no scenarios, ask about the happy path and one or two real edge cases of K5. For a flow with only a happy path, ask about the obvious edge case.
- view or next: A missing screen or view. Ask only if the slice itself shows the gap, such as a command with no screen or a view that feeds nothing. A part of the story that the model has not reached yet is not a gap.
- who: Who does this, who is allowed to, and can one person act for another?
- time: Does the order of the steps matter? Is there an implied deadline, timeout, or recurring step?
- data: Ask only if a later element needs data that is not there. Do not ask about identifiers, timestamps, or version numbers.
- action, data, next: For a button with no action, a field that nobody stores, or a result with no next step. Tell the person that an example answer becomes a future scenario (K11).

## Rules

1. Write each question as a product manager talks to a stakeholder. Never use these words: event, command, read model, slice, actor, spec, scenario, given, when, then, modeled, "not modeled". Never name a shape.
2. Say "this step", "this action", "what the person sees", "who does this", and "what do we expect when".
3. Do not question a design choice that the model clearly makes on purpose.
4. Do not invent requirements that the model does not support. Do not assume that a notification is missing.
5. Keep each question to one short sentence. Be curious and direct, like someone who saw these flows break in production.
6. Do not try to be complete. One question for each element is the default (K11).

Read `references/examples.md` when you need sample questions.

## Result

The skill writes one open question record with a category for each question, on the element it is about. It changes no element and no other record.

It reports to the person:

1. The questions in story order, each with its element and its category.
2. A short summary: how many flows you read, how many questions you wrote, and the main themes as business questions.
3. One next step, if a clear gap exists. If no question holds up, it says so in one line.

## Done when

1. Each question is about something unclear or missing, and the model shows the reason for it.
2. No question uses a banned model word or a shape name.
3. Each question is an open question record on its element, with one of the eight categories.
4. The questions follow story order, with no jump back.
5. The shape review ran once for the whole model.
6. No question repeats an open question that already existed.
7. Zero questions is reported in one line when nothing holds up.
8. No element of the model changed.
