---
name: eventmodeling-translating-external-events
description: Maps the payload of each event from another system to the business fields of the internal event that its translation step records, with correlation on our side, a duplicate rule, and a class for each missing field. Use it when someone shares a webhook or partner payload and asks how its fields map into the domain, how to link an external identifier to an order, or how to handle a repeated delivery. Does not write automations, todo lists, events, or scenarios.
metadata:
  version: "1.0.0"
  contract: "K0 K2 K6 K8 K9 H0 H7 H8 H10"
---


# Translating external events

This skill fills each translation step with a field mapping. A payload is the raw data that another system sends. After this skill, every payload field maps to a business field or has a reason to stay out, and no external identifier is a domain key. The skill writes the external mappings part only.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read these parts of the model:

- roles: the external systems that send data
- events: each event from another system and the internal event of its translation step
- automations: the translation step of each external event
- commands: the commands that start an action in the external system

Also read a sample payload for each external event type, from a document or from the person.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

If an external event has no translation step, map nothing for it. Write a request (K8) on the event, concerning automations.

## Procedure

1. Resolve each open request on your part first.
2. List the external systems, their event types, and their data formats.
3. Get one sample payload for each event type. If none exists, ask the person for one (K9).
4. Mark opaque identifiers, values in foreign units or formats, and fields that stand for a business fact.
5. Map each payload field to a business field of the internal event. Give each field its origin under K2.
6. If the internal event lacks a field that the business needs, write a request on the event, concerning events.
7. Decide correlation on our side: store a reference when our command starts the external action, or send our identifier so that the external system returns it.
8. Keep the external identifier as a plain field and mark it as the duplicate key. A second delivery with the same value records nothing new.
9. Mark each business field that the payload does not supply as enrich, ignore, or infer. Enrich means look it up in our own data. Ignore means the domain does not need it. Infer means a safe value follows from the event itself. Write the reason for each inferred value.
10. Pick one integration pattern for each event type from the rules.
11. List the failure cases: missing correlation, wrong state, duplicate delivery, and invalid business data. Write them as a request on the translation command, concerning command scenarios.

## Rules

1. No external identifier is a domain key.
2. Correlation lives on our side. Never depend on the external system to know our identifiers, unless it returns one that we sent.
3. Enrich from our own data, not from the external system.
4. Translate the business meaning, not only the field names. The internal event never copies the shape of the payload.
5. Every missing field has exactly one class: enrich, ignore, or infer.
6. The integration patterns are:
    1. Simple mapping: the payload holds every needed fact.
    2. Correlation lookup: the payload holds an external identifier. Look up our entity, then map.
    3. Polling: our system asks the external system on a schedule. Each answer is a payload to translate.
    4. Enrichment: the payload holds part of the facts. Look up the rest in our own data.

## Result

This skill writes the field mapping of each external payload, the correlation key, the duplicate key, and the class of each missing field, plus their records (K8). It reports to the person a table for each event type: payload field, business field, class, and the integration pattern, and the requests it wrote.

Read `references/examples.md` for a worked payment mapping.

## Done when

1. Every external event type with a translation step has a sample payload and a field mapping to its internal event.
2. Every external event type has a correlation method on our side, and no external identifier is a domain key.
3. Every internal event keeps the external identifier as its duplicate key.
4. Every missing field is marked enrich, ignore, or infer, and each inferred value has a reason.
5. Every external event type has one integration pattern.
6. The failure cases are written as a request concerning command scenarios.
7. Each open request on the external mappings part is resolved.
