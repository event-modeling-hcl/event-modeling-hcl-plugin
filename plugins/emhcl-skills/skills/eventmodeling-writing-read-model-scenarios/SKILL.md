---
name: eventmodeling-writing-read-model-scenarios
description: Writes view scenarios and storylines for read models and todo lists. A view scenario shows what a view displays after given events. A storyline walks one view through several states in order. Use it when someone asks what a list, a total, a dashboard, or a todo list shows after certain things happen, or asks for test cases of a view. Does not write command scenarios. Does not change read models or events. Does not measure coverage.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K2 K5 K6 K8 K9 H0 H9 H10"
---

# Writing read model scenarios

This skill gives each read model a view scenario or a storyline, or both. A view scenario is one test: given events, then the read model shows given values. A storyline is one ordered walk of a read model through several states. The skill writes one part: read model scenarios.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- read models, their fields, and the events that feed them
- todo lists of automations, which are read models (K2)
- the chapter of each feeding event

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

If a read model or one of its feeding events does not exist, write no scenario for it. Write a request (K8) on the nearest element, concerning read models.

## Procedure

1. Resolve each open request on your part first.
2. Decide the format of each read model before you draft any scenario. Choose "storyline", "view scenarios only", or "storyline and view scenarios". Write one line for each read model in your report: the name, the format, and a reason in one clause.
3. For each case of K5 for a read model (appear, change, disappear) that applies, write one view scenario, unless a storyline beat will show that case.
4. In a view scenario, put the feeding events in the given step. Leave the when step out. Put the read model with its expected values in the then step.
5. For a list, write each expected row with its values. If the list is empty on purpose, state that the list is empty.
6. If the format includes a storyline, write it with the beat grammar below.
7. Read the beats again. Remove each view scenario that asserts a state that a beat already shows. Fix or remove each view scenario that contradicts a beat.
8. If the feeding events live in another chapter, write the scenario with no given event. Say in the title that the source is in that chapter. Do not invent an event to fill the gap.
9. Fill each essential value under K6.
10. If the source is code, write a storyline only when the person asks for it.

### Format decision

Choose a storyline when the replay of the feeding events gives a state worth telling. One event that repeats with new data counts too. A balance that grows with each deposit is a storyline case. A todo list is a typical case: a row appears when work opens and leaves when work ends. Choose view scenarios only when each event gives one plain result.

### Beat grammar

1. The first beat shows the read model in its start state, often empty.
2. Each next beat names one event, then the new state of the read model with its values.
3. An error beat can show a command that the system refuses. The state of the read model after it stays the same.
4. The last beat shows the end state of the walk.

## Rules

1. Each read model has at least one view scenario or one storyline.
2. The format decision comes before the first draft and appears in the report.
3. The view scenarios and the storyline of one read model never repeat or contradict each other.
4. A read model used in two places is one read model (K1). Its scenarios exist once.
5. A note is the last resort. Use a note only for background that no event or read model field can hold.

Read `references/examples.md` before you write the first scenario.

## Result

This skill writes view scenarios and storylines on read models and todo lists. It writes requests on elements of other parts. It changes no other part.

It reports to the person: the format decision of each read model with its reason, the scenarios and storylines it wrote, and each request.

## Done when

1. The report holds a format decision with a reason for each read model.
2. Each read model has at least one view scenario or one storyline.
3. Each read model whose format includes a storyline has that storyline.
4. Each list expectation names its rows or states that the list is empty.
5. No view scenario repeats or contradicts a storyline beat of the same read model.
6. Each scenario of a read model fed from another chapter says so in its title, and no invented event stands in for its source.
7. Each asserted value has a concrete example.
8. No open request on read model scenarios remains.
