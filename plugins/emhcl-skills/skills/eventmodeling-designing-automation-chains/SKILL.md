---
name: eventmodeling-designing-automation-chains
description: Designs each automation's processor and pending-work read model, puts translation before decisions on another team's or system's facts, and identifies a following worker only for a new decision. Use it when someone asks what the system does on its own, how a scheduler reacts to events, or how a webhook enters the process. Writes automations and their todo lists. Requests commands and events from their writers. Does not write external field mappings, screen read models, commands, events, or scenarios.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K2 K3 K8 K9 H0 H3 H7 H10"
---


# Designing automation chains

This skill designs automation structure and pending work under K3. It identifies which command the processor must issue and which internal fact that command must record. Their writers supply those elements under K0. The skill writes the automations part only.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read these parts of the model:

- roles: the system actors inside and outside the system
- events: every event, its system, its context, and its owner team
- commands: the commands that automations issue
- read models: derived values that screens show

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

## Procedure

1. Resolve each open request on your part first.
2. List every automation and every request concerning automations.
3. For each automation, name the event that triggers it. If the trigger is only an informal signal, write a request (K8) concerning events for a real event.
4. If the trigger belongs to another team or system, design a translation step under K3. Its foreign facts feed its todo list. The internal result never closes that projection.
5. Identify the translation command and its internal success event. Request them from their respective writers. The command validates the mapping without making a new business decision.
6. Propose the internal fact's business name in its event request. Reuse the foreign name only when the receiving domain uses that term. Avoid transport names such as "Received", "Signal", or "Synced".
7. Leave the field mapping of the payload to the external mappings part.
8. Decide whether a worker step follows. Add one only when a new decision remains: a rule to test, a choice, or a new value to compute.
9. If the internal event already is the whole business fact, end the chain there. Other consumers read it through a read model.
10. For every worker step, design its todo list. Name the events that open an item and the events that close it. The result event of the worker itself is one closing event.
11. If a foreign fact opens a local worker's list directly, insert translation first. A foreign team's context can remain internal to the modeled system.
12. Give each todo list field an origin under K2. A row holds the identity of the open item and the data needed to act.
13. For each derived business condition, ask: does a domain expert name this fact, and does a later step react to it? Ask the person (K9) when you cannot tell.
14. If both answers are yes, request the derived fact from the events writer and design the processor whose pending work its causes open.
15. If causes mean the same thing to the business, request their merge from the events writer. Keep distinct meanings separate.
16. If the condition is only shown on a screen, leave it as a read model field.
17. Request every missing command and event from its part's writer. When it exists, connect the processor and its todo list without moving it to another slice.
18. Review the structure under K3. Report pending requests and boundary gaps. Never report the whole chain complete while a required command or event is missing.

## Rules

1. Apply the shared pending-work and translation rules of K3. A minimal legal encoding exception does not complete this method task.
2. Ask these questions for each step:
   1. Which evidenced fact opens this work?
   2. Which business question does its todo list answer?
   3. Does it translate a foreign meaning or make a local decision?
   4. Which command must its processor issue?
   5. Which writer owns a missing field, command, or event?
   6. Do its scenarios distinguish dispatch, refusal, and completion?
3. For an internal cross-team translation, preserve the ownership boundary even when a CLI classifies the step as a worker (H7).

## Result

This skill writes processors, their todo lists, and worker and translation structure, plus their records (K8). In an `.em.hcl` model, it creates each `automation` workflow and requests its chapter and board position (H3). Commands and events remain with their writers. The report names each step, its business responsibility, its review result, and outstanding requests.

Read `references/examples.md` for a worked translation and worker chain.

## Done when

1. Every fully modeled automation has pending work under K3, and its trigger is a real fact.
2. Foreign facts pass translation before local worker decisions, including across internal team boundaries.
3. Each required internal event has a business name or an explicit request to its writer.
4. Each worker makes a new decision and has the opening and closing facts that K3 requires.
5. No todo list has a status field.
6. Each derived business condition has domain evidence and a later consumer, or stays a read model value.
7. The report gives each review result, boundary gap, and pending request. It does not claim completeness while a required command or event is missing.
8. Each open request on the automations part is resolved or names its blocked prerequisite.
