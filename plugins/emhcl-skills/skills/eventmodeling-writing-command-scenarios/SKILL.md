---
name: eventmodeling-writing-command-scenarios
description: Writes given-when-then scenarios for each command and each automation action, one for each meaningful case, with concrete example values and rejections in domain words. Use it when someone asks to write test cases or acceptance criteria for an action, to turn business rules or limits into scenarios, or to show what happens when an action is refused. Does not write read model scenarios or storylines. Does not change commands, events, or lifecycles. Does not measure coverage.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K5 K6 K7 K8 K9 H0 H9 H10"
---

# Writing command scenarios

This skill gives each command a set of scenarios. A scenario is one test: given past events, when a command arrives, then new events or an error. Each meaningful case of the command gets its own scenario, and each business rule of the source gets at least one. The skill writes one part: command scenarios.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- commands, their fields, and the events they produce
- lifecycles: the states, the moves, and the refused moves of each stream
- automations, when an automation issues a command
- the source: business rules, deadlines, and limits in documents, and tests and comments in code

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

If a command or its events do not exist, write no scenario for it. Write a request (K8) on the nearest element, concerning commands.

## Procedure

1. Resolve each open request on your part first.
2. List the rules that apply to the command. Take them from the source, from the lifecycle, and from the tests.
3. For each case of K5, ask if the business supports it for this command. If the domain says that a case cannot occur, write the reason in one clause in your report.
4. For each case that applies, write one scenario. Use the success shape or the rejection shape below.
5. Take each refused move of the lifecycle. Write one rejection with the case "state violation" (K7).
6. Fill each essential value under K6.
7. Give the scenario a title that names the rule in business words.
8. Put the scenario on the command that it tests. A command used in two places is one command (K1), so write its scenarios once.
9. Match each source rule to at least one scenario. If a rule has no scenario, write one.
10. If the source leaves part of an outcome undefined, cover only its known part in the scenario. Record the missing part as an open question (K8) on the command.
11. If a rule needs a value that no element carries, write a request (K8) on that element, concerning its part. Do not move the value into a note.
12. If the lifecycle has no refused move for a wrong state that a rule names, write a request (K8) on the lifecycle, concerning lifecycles.

### Success shape

- Given: the events that make the start state. This list can be empty for a first action.
- When: the command with its example values.
- Then: each event that the command produces, with its example values.

### Rejection shape

- Given: the events that make the wrong state. This list can be empty when the business refuses the input itself.
- When: the command that the system refuses.
- Then: no event.
- Error: the reason in domain words, as a user reads it.

### Automation actions

- Given: the events or todo list rows that make the automation act.
- When: the automation.
- Then: the command that it issues, with its values. If it issues nothing, say so.

### Rules from different sources

- From a document: each rule fact gives a success scenario. If the rule can be broken, it also gives a rejection.
- From code: take only business rules from tests and comments. Do not copy a test line by line. Mocks and setup calls never become steps.
- From an event of another system: write a scenario for each failure of the translation that the business cares about, such as no match to a known item.

## Rules

1. A command always uses given-when-then. A command never gets a storyline.
2. The error text is a short reason that a user can read, such as "The trip is already closed". It is never an identifier, a placeholder, or a cut value.
3. Each given step names its exact state. Write "given a rental that started at 09:00", not "given a rental".
4. The when step says who acts and what they do.
5. The then step names each event and its values, or the error. "It works" and "there is an error" are not outcomes.
6. Use a note only for background that cannot fit in an event, a command field, or a read model.

Read `references/examples.md` before you write the first scenario.

## Result

This skill writes command scenarios on commands and on automation actions. It writes open questions on commands for rules that the source leaves incomplete, and requests on elements of other parts. It changes no other part.

It reports to the person: the scenarios per command, each case that the domain excludes with its reason, and each open question and request.

## Done when

1. Each case of K5 for each command has a scenario, or the report gives a reason why the domain excludes it.
2. Each rule in the source has at least one scenario.
3. Each refused move of a lifecycle has a scenario with the case "state violation".
4. Each rejection has no event in its then step and an error in domain words.
5. Each essential value (K6) has a concrete example.
6. Each title names the rule in business words.
7. No scenario tests a technical case of K5.
8. No note holds a fact that a step can hold.
9. No open request on command scenarios remains.
