---
name: eventmodeling-designing-automation-chains
description: Gives every automation a todo list and a real triggering event, puts a translation step in front of each event that comes from another system, decides when a worker step with a new decision follows, and decides when a derived business condition earns its own event. Use it when someone asks what the system does on its own, how a scheduler or background job reacts to events, or how a webhook or partner message enters the process. Does not write external field mappings, screen read models, commands of screens, or scenarios.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K2 K3 K8 K9 H0 H3 H7 H10"
---


# Designing automation chains

This skill gives each automation a todo list and a clear trigger. A todo list is a read model of open work. After this skill, every worker automation reacts to internal events only, and every event from another system passes a translation step first. The skill writes the automations part only.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read these parts of the model:

- roles: the system actors inside and outside the system
- events: every event, and which system owns it
- commands: the commands that automations issue
- read models: derived values that screens show

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

## Procedure

1. Resolve each open request on your part first.
2. List every automation and every request concerning automations.
3. For each automation, name the event that triggers it. If the trigger is only an informal signal, write a request (K8) concerning events for a real event.
4. If the trigger is an event from another system, build a translation step first. Give it its own todo list. The external event opens the list. Nothing closes it.
5. Give the translation step one command and one internal event. The command makes no business decision. It records the outside fact in business words.
6. Give the internal event a business name. Reuse the external name only if the business already uses that term. Add no transport word such as "Received", "Signal", or "Synced".
7. Leave the field mapping of the payload to the external mappings part.
8. Decide whether a worker step follows. Add one only when a new decision remains: a rule to test, a choice, or a new value to compute.
9. If the internal event already is the whole business fact, end the chain there. Other consumers read it through a read model.
10. For every worker step, design its todo list. Name the events that open an item and the events that close it. The result event of the worker itself is one closing event.
11. If an external event opens a worker todo list, split the step into a translation step and a worker step.
12. Give each todo list field an origin under K2. A row holds the identity of the open item and the data needed to act.
13. For each derived business condition, ask: does a domain expert name this fact, and does a later step react to it? Ask the person (K9) when you cannot tell.
14. If both answers are yes, model the condition as its own event, produced by an automation whose todo list the causing events open.
15. Fold only causes that mean the same thing to the business. Keep causes with other meanings as separate events.
16. If the condition is only shown on a screen, leave it as a read model field.
17. If a command or an event that the chain needs does not exist, write a request on the nearest element, concerning commands or events.
18. Run the review in the rules for every automation and report the result.

## Rules

1. Every automation has a todo list. A simple relay is no exception.
2. Opening events and closing events of a todo list can differ in number and in kind.
3. Only a translation step reads a todo list that an external event opens.
4. A translation step never closes its todo list and never decides anything.
5. Two automations in a chain exist only when two steps exist: the translation, which decides nothing, and the worker, which decides.
6. The review for each automation asks:
    1. Does it read its own todo list?
    2. Do internal events alone open it, unless it is a translation step?
    3. If it is a translation step, is its todo list free of closing events?
    4. If it is a worker after a translation step, does its command make a new decision?
    5. If it is a worker, does its own result event close its todo list?
    6. Is the todo list free of a status field?

## Result

This skill writes automations, their todo lists, translation steps with their command and internal event, and the automations of derived conditions, plus their records (K8). In an `.em.hcl` model it creates the `automation` workflow of each one, with requests for the chapter and the board (H3). It reports the review result for each automation and the requests it wrote.

Read `references/examples.md` for a worked translation and worker chain.

## Done when

1. Every automation reads its own todo list, and every trigger is a real event in the model.
2. Every event from another system opens only a translation step, and no translation step has a closing event or a business decision.
3. Every internal event has a business name.
4. Every worker step makes a new decision, and its own result event closes its todo list.
5. No todo list has a status field.
6. Every derived condition with its own event has a business name and a step that reacts to it.
7. The review result is reported for each automation.
8. Each open request on the automations part is resolved.
