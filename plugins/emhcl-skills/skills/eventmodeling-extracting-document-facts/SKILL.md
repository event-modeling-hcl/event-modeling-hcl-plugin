---
name: eventmodeling-extracting-document-facts
description: Reads a document or an image, such as a tender, a contract, a specification, or a process description, and records each fact that it holds as evidence in the model, with a precise location and a certainty. Each fact becomes evidence on an element, a request on the element for the part that must change, an open question, or a decision that leaves it out with a reason. Use it when someone asks to build or extend an event model from a document, to pull the facts out of a PDF or a picture, or to make sure that a model covers everything a document says. Does not write events, commands, screens, read models, scenarios, or any other model part. Does not read source code.
metadata:
  version: "1.0.0"
  contract: "K0 K6 K8 K9 H0 H10"
---

# Extracting facts from a document

This skill makes sure that each fact of a document reaches the model or a recorded decision to leave it out. It writes records only: one evidence source for each document, evidence, requests, open questions, and decisions. It writes no element of any model part. The ledger of facts goes into the reply to the person, never into a file.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- the source: one or more files, a web page, or an image, as one package
- the perspective: the party whose work the model describes, for example the bidder or the buyer
- the focus: the parts to cover or to skip (default: the whole source)
- the current model, with its evidence sources and evidence from earlier runs on the same source

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

If no source is given, ask for it under K9 and stop.

## Procedure

1. Resolve each open request on the records of this source first.
2. Decide the perspective. If the source does not make it clear, take the most likely one and record it as an assumption (K8). Do not wait for an answer.
3. Write one evidence source of the kind document for each file. Its location names the file. If an earlier run wrote it, reuse it.
4. Read the whole source in scope, not only the table of contents. Read a long source in parts of about 20 pages. Finish the facts of one part before you read the next part.
5. For an image, write down all visible text first. Then read the structure: boxes and arrows show a flow, and tables show data.
6. Give each fact an id, a kind from the table under "Fact kinds", a statement, a location with section and page, and a certainty (K8).
7. Copy each number, threshold, weight, date, and named document word for word (K6, K8).
8. If two passages contradict each other, write one open question that names both locations (K9). Do not choose a side.
9. For each fact, find the element of the model that it supports. If the element exists, write an evidence record on it.
10. If the element does not exist or must change, write a request (K8) on the closest element, concerning the part that must change. Use the table under "From fact to part". A request about the whole model has no element.
11. For each rule and each deadline, write a request concerning command scenarios or read model scenarios. Name the verbatim values, one case that passes, and one that the business refuses. For a threshold, name one value on each side.
12. If the outcome of a rule depends on a part that the source does not define, request the stated part only. Record the gap as an open question.
13. Run the coverage pass. Go through the facts one by one. Each event, deadline, rule, and requirement has evidence on an element, an open request, an open question, or a decision.
14. For each fact that the model leaves out, write a decision with its reason (K8 rule 12), such as "out of focus" or "boilerplate".
15. Report to the person under "Result".

## Fact kinds

| Kind | What it holds |
| --- | --- |
| actor | a person, a role, an organization, or a system |
| process | an ordered flow of work |
| event | something that happened, in the past tense |
| deadline | a date, a duration, or a time window |
| rule | a condition, a limit, or a decision criterion |
| requirement | something the solution or the bidder must deliver or prove |
| data | a document, a form, or a set of fields that people exchange |
| unknown | a missing, contradictory, or unclear item |

## From fact to part

| Fact kind | Part that the request concerns |
| --- | --- |
| actor | roles |
| event, or a deadline that passes | events |
| process step that a person does | screens and commands |
| deadline that starts work by itself | automations |
| event of another organization | external mappings |
| rule | commands or read models, and the scenario part |
| requirement | read models or commands |
| data | the part of each element that carries the field |
| process order or journey | story order or chapters |

## Rules

1. The source is the authority. If the source says nothing, the model says nothing. General domain knowledge becomes an open question or an assumption, never stated evidence.
2. Keep the source confidential. Do not upload it to any other place.
3. On a run over a source that the model already cites, read its evidence first. Add new facts. For a changed fact, write a request on its element.
4. If the source needs more elements than expected, write the requests. Tell the person about a real scope trade-off. Never drop a fact in silence.

Read `references/examples.md` when you need a worked ledger and a coverage pass.

## Result

The skill writes evidence sources, evidence, requests, open questions, assumptions, and decisions for items left out. It writes no element.

The reply holds, in this order:

1. the open questions
2. the perspective and its certainty
3. the ledger table: id, kind, statement, location, certainty, and the record that covers the fact
4. the requests, grouped by the part that they concern
5. the items left out, with their reasons

## Done when

1. Each fact in the ledger table has an id, a kind, a statement, a location with section and page, and a certainty, and no assumption carries the certainty stated.
2. Each event, deadline, rule, and requirement has evidence on an element, a request, an open question, or a left-out decision with a reason.
3. Each number, date, and threshold matches the source word for word.
4. Each contradiction is one open question that names both locations.
5. Each rule has a scenario request with values on both sides of each threshold.
6. The model holds one evidence source of the kind document for each file of the source.
