---
name: eventmodeling-reading-code-evidence
description: Reads an existing code base through four lenses (API, tests, persistence, user interface) and records what it finds as evidence and requests in the model, each with a precise code location. The code gives hypotheses, and the person decides what is true. Each pass over the code is recorded as an evidence source with its commit. Use it when someone asks to reverse engineer a legacy system, to build an event model from an existing application or repository, or to find the business process behind the code. Does not write events, commands, screens, read models, scenarios, or any other model part. Does not read documents. Does not compare an existing model with later code changes.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K8 K9 H0 H10"
---

# Reading evidence from code

This skill finds the business process behind existing code. The code gives hypotheses, and the person gives the truth. The skill writes records only: one evidence source of the kind code for each pass, evidence with code locations, requests, open questions, and decisions. It writes no element of any model part.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- the code root, which must hold source code
- the current model, if one exists
- the evidence sources of kind code from earlier passes, for each chapter in scope

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

If the folder holds no source code, tell the person in one sentence and stop.

## Procedure

1. Resolve each open request on the records of earlier code passes first.
2. If the model is shared with other people, ask for consent before the first change. Say that the model will hold file paths and class names. If the person says no, stop and change nothing.
3. Find the baseline of each chapter in scope: its latest code pass (K8 rule 24). Read only the files that changed since its commit. If no pass exists, or the commit is not reachable, read the chapter in full.
4. Ask once whether a running system exists to inspect. Continue with the code at once.
5. Read the code through the four lenses under "Four lenses". Each lens gives hypotheses, never elements.
6. Map each hypothesis with the table under "From code to part". Start with the API and persistence lenses. Use tests and the user interface to confirm and to name.
7. If the lenses disagree, write an open question. Examples are a route that nothing calls, a table that nothing writes, or a test for removed behavior.
8. If the system only reads a record and never writes it, treat it as reference data. Ask where it comes from. Do not request an event for it.
9. If the code is a generic engine, request one real case that it handles, not the engine (K1).
10. Ask the person when the code does not show the order of steps. Never request a step at a guessed position.
11. Group by user journey, not by endpoint. Registering, finding, and updating a customer belong to one journey. Request the grouping concerning chapters.
12. For an element that exists, write evidence with the code location and a certainty. For a confirmed hypothesis with no element, write a request (K8) on the closest element, concerning the part that must change. Use business names in the request and code names in the location (K8 rule 20).
13. Write a decision for each merge, rename, override by the person, and item left out.
14. Write one evidence source of the kind code for this pass under K8 rules 21 and 22. Write it also when the pass found nothing new.
15. Report under "Result". Ask which chapter to read next, or whether to stop.

## Four lenses

| Lens | What to read | What it suggests |
| --- | --- | --- |
| API | inbound routes and handlers, listeners for messages, outbound calls, jobs that run on a schedule | screens with actions or views, automations |
| Tests | test names, fixtures, assertions | business words, rules from error cases, example values |
| Persistence | tables, entities, migrations, repositories | events from writes, lifecycles from status values, read models from joins |
| User interface | templates, views, forms, navigation | where a person decides, the page order, the business words |

The arrange, act, and assert parts of a test are only a hint for given, when, and then.

## From code to part

| In the code | Hypothesis | Part that the request concerns |
| --- | --- | --- |
| a write that saves or changes state | an event with the saved fields | events |
| a status column or enum | states and moves of a stream | lifecycles |
| an inbound call that a person starts from a form | a screen and a command | screens, commands |
| an inbound call that a person starts to see data | a screen and a read model | screens, read models |
| a job, a listener, or a webhook | an automation and its command | automations |
| a message from another system | an external event and its mapping | external mappings |
| a query or a join | a read model, fed by the events behind its tables | read models |
| a test of a business rule | a scenario | command scenarios or read model scenarios |

Several writes in one call are one decision, possibly with several events. Ask the person.

## Detail per layer

A layer is one level of detail in a pass over a chapter. Never request detail that belongs to a deeper layer.

| Layer | Elements | Fields | Scenarios |
| --- | --- | --- | --- |
| 0 | one chapter for each journey, milestones only | none | none |
| 1 | the real command, event, and read model sequence of one journey | key fields only | happy path and the one or two main rules |
| 2 and deeper | sub-flows, other paths, automations | the full business field set | error cases and edge rules |

At layer 0, report the chapters and let the person choose the first one.

## Rules

1. The person outranks the code (K8 rule 17).
2. Take scenarios from tests only for business rules. Leave out input format rules such as "must be a number".
3. A mock, a repository, or a setup call in a test is never a scenario step.
4. Submit forms only in a local environment or a test environment. On another system, obtain permission from the person first.

Read `references/examples.md` when you need a worked mapping with code locations.

## Result

The skill writes one evidence source of the kind code for the pass, evidence, requests, open questions, and decisions. It writes no element.

The reply holds the open questions first, then a ledger table (lens, code location, hypothesis, certainty, record), the requests grouped by part, the sub-flows found, and the location of the new evidence source.

## Done when

1. Each evidence record from the pass has a code location with path from the code root and line, and a certainty.
2. The model holds one new evidence source of the kind code for this pass, with the code root, the short commit (or "+dirty" or "no git"), the date, the pass number, the scope, and the result.
3. Each conflict between the person and the code follows the person, and the code behavior is a decision.
4. Each disagreement between lenses is an open question.
5. No request places a step at a guessed position, and no request holds detail from a deeper layer than the pass.
6. No evidence source of an earlier pass changed.
