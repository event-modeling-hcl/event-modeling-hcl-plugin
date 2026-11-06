---
name: eventmodeling-applying-answers
description: Turns each answer from a business person to an open question of the model into a decision and a request for the part that must change, chosen by the category of the question. It marks the answered question as resolved. An answer that contradicts the model goes back to the person as a question. Use it when someone brings back answers from a workshop, a prototype tour, or a review, or says "here are the answers to your questions". Does not write events, commands, screens, read models, scenarios, or any other model part. Does not write new questions for a tour. Does not handle free comments that answer no question.
metadata:
  version: "1.0.0"
  contract: "K0 K8 K9 K11 H0 H10"
---

# Applying answers to the model

This skill takes the answers to open questions of the model and records them. Each answer becomes a decision with the person as source, a request on the element for each part that must change, and a resolved status on the question. It writes records only, never an element of any model part. An answer that contradicts the model never changes anything in silence.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- the answers, each with its question, its category (K11), and the element it is about. The question can be an open question record of the model or a question from a tour report.
- the name of the person who answered
- the model: the element of each question and its neighbors

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

## Procedure

1. Collect the answers. A question that the person left open stays open.
2. For each answer, find the element that the question was about. If the element is used in two places, it is one element.
3. Compare the answer with the model. If it contradicts a fact, a rule, a scenario, or another answer, write nothing for it. Go to step 8.
4. If the answer names no result, treat it as ambiguous (K9). Go to step 8.
5. Write a decision with the answer, its reason, and the person as source (K8 rule 10). Write evidence of certainty stated on the element. If the answer confirms an assumption, change the certainty of that assumption to stated (K8 rule 16).
6. Write one request (K8) on the element for each part that must change. Pick the part with the table under "Rules". Name the decision in the request.
7. Mark the question as resolved. Keep the question record.
8. Collect each contradiction and each ambiguous answer as a question back. Put all of them in one message (K9) with options.
9. Report under "Result".

## Rules

1. Map each category to the part that the request concerns:

| Category | Request on | Part that the request concerns |
| --- | --- | --- |
| rule | the element of the question | command scenarios or read model scenarios |
| example | the element of the question | command scenarios or read model scenarios |
| data, on a screen | the screen | screens |
| data, on an action | the command | commands |
| data, on a fact | the event | events |
| data, on a display | the screen | read models |
| next, a screen | the screen of the question | screens |
| next, a fact | the element of the question | events, and story order |
| next, a reaction | the element of the question | automations |
| view | the screen | read models |
| action | the screen | commands |
| who | the element of the question | roles |
| time | the element of the question | command scenarios, or automations for work that starts by itself |

2. A rule or example request names the element of the question. Never move it to another element. Give it the given, when, and then of the answer, with values under K6.
3. A next answer that adds a step asks for a new step after the element of the question. Never ask to squeeze it into that element.
4. A next answer that names a screen the model does not have leaves an open end. Write it as an open question of category next on the element of the question.
5. Each request traces to one answer. Write no request that no answer asked for.
6. If several answers touch one element and one part, put them in one request.

Read `references/examples.md` when the category of an answer is not obvious.

## Result

The skill writes decisions, evidence, requests, and the resolved status of answered questions. It writes no element.

The reply holds one line for each answer: the answer in short, the element, the decision, and the parts that the requests concern. Then it holds the questions back, in one block.

## Done when

1. Each request names one answer through its decision, and each answered question is resolved and still present.
2. Each rule or example answer is a request concerning a scenario part, on the element of its question.
3. Each contradiction is a question back, and the model holds no decision or request for it.
4. Each question that the person left open is still open.
5. Each applied answer is a decision that names the person.
