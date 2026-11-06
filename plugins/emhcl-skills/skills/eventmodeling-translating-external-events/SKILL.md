---
name: eventmodeling-translating-external-events
description: Maps facts from another team or system to the receiving domain's fields, with local correlation, duplicate behavior, and evidenced conversions. Use it for webhook and partner payloads, cross-team translation contracts, foreign identifiers, and repeated delivery. Writes external mappings only. Does not write automations, todo lists, commands, events, or scenarios.
metadata:
  version: "1.0.0"
  contract: "K0 K2 K3 K5 K6 K8 K9 H0 H7 H8 H10"
---


# Translating external events

This skill fills translation steps with field mappings. A foreign payload carries another team's or system's facts. Apply K3 to preserve its business meaning and local identity. An internal context can still supply a foreign team's facts. The skill writes the external mappings part only.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read these parts of the model:

- roles and ownership: the teams and systems that own foreign facts
- events: each foreign fact and the internal fact that its translation records
- automations: the translation step of each foreign fact, including internal cross-team steps
- commands: the commands that start an action in the external system

Read the available payload evidence for each foreign event type, whether the owner is another team or an outside system.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

If a foreign fact has no translation step, map nothing for it yet. Request the automations part under K8.

## Procedure

1. Resolve each open request on your part first.
2. List the foreign teams and systems, their event types, and their data formats.
3. Find a sample payload for each event type in the sources. If none exists and mapping needs it, follow K9.
4. Mark opaque identifiers, values in foreign units or formats, and fields that stand for a business fact.
5. Map each payload field to a business field of the internal event. Give each field its origin under K2.
6. If the internal event lacks a field that the business needs, write a request on the event, concerning events.
7. Establish local correlation under K3. If a pairing fact or outward reference is missing, request its owning command or event. Never add those fields yourself.
8. Identify the foreign reference used for deduplication. Request any required key fields or annotations from their command or event writer. Preserve the supplied repeat behavior under K5.
9. Classify each foreign field as copied, enriched, ignored, or inferred under K3. For each needed local field absent from the payload, state its local source or inference rule. Record an unknown source as a question.
10. Pick the integration pattern supported by the evidence. Document conversions as derivations without changing the source's original values.
11. Identify meaningful failure cases under K5, including missing correlation, wrong state, and duplicate delivery. Request their command scenarios. Do not invent a failure rule or error text.

## Rules

1. Apply the identity, correlation, and field-classification rules of K3.
2. Mapping ownership does not permit changing command or event contracts. Request missing fields, key annotations, and acceptance rules from their writers.
3. Use the evidenced integration pattern:
   1. Simple mapping: the payload supplies each needed fact.
   2. Correlation lookup: a foreign reference locates the local entity.
   3. Polling: scheduled work obtains a payload to translate.
   4. Enrichment: local facts supply missing meaning.
4. Polling describes the interaction, not permission to design infrastructure.

## Result

This skill writes field mappings and documented derivations, plus their records (K8). It reports each foreign event type, its field classes, correlation method, deduplication rule, integration pattern, and requests. Command and event writers retain their key fields and annotations.

Read `references/examples.md` for a worked payment mapping.

## Done when

1. Each foreign event type in scope has an evidenced mapping to its receiving domain's fact.
2. Correlation and field classification follow K3, including facts from another team inside the modeled system.
3. Required correlation and duplicate keys exist on their owning elements, or requests name the missing contracts.
4. Every inference and conversion states its source and rule.
5. The integration pattern comes from evidence.
6. Meaningful failure scenarios are requested under K5. Unknown outcomes remain questions.
7. Each open request on the external mappings part is resolved.
