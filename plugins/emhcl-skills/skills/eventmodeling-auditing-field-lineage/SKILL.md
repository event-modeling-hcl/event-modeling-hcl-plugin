---
name: eventmodeling-auditing-field-lineage
description: Audits every field in the whole event model for a missing origin or a missing consumer, and lists each gap once with the search that was made for the data. Use it when someone asks where data in the model comes from, which fields appear from nowhere, which inputs are never used, or whether the data flow of the model is complete. Writes nothing in the model until the person confirms a fix, then writes requests only. Does not add or rename fields. Does not trace one piece of data for a person.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K2 K8 K9 K10 H0 H8 H10"
---

# Auditing field lineage

This skill gives one list of field gaps across the whole model. A field gap is a field with no origin or a field with no consumer. The skill searches for the data elsewhere in the model before it reports a gap. It writes nothing in the model during the audit. After the person confirms a fix, it writes requests only.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs: every chapter of the model, and each element with its fields and its connections: screens, commands, events, read models, automations, and translation steps. Read the scenarios too, because a scenario can show where a value comes from. Read the decisions, because a recorded decision or debt can explain a gap (K10).

An origin is one of the four origin states of K2. A consumer is an element downstream that uses the field.

If the model is an `.em.hcl` file or folder, read origins as H8 describes: same names, `field_source` blocks, and `generated = true` for a value that the system fills.

## Procedure

1. List every field on every element in the model. Cover all chapters, not only one.
2. For each field, find its origin under K2. Look only upstream (K2 rules 7 to 9).
3. For each field, find its consumers downstream: events, read models, screens, automations, or another system.
4. For each command field, make sure that the value reaches at least one resulting event, directly or as part of another fact.
5. For each read model field, make sure that a feeding event carries its source, or that the read model computes it (K2 rule 16).
6. For each field that a screen shows, make sure that the read model behind the screen carries it (K2 rules 18 to 21).
7. If a field seems to have no origin, search the rest of the model for the same data: other chapters, other names, and scenarios.
8. If you find the data elsewhere, record the real origin and the missing link. Do not report the field as missing data.
9. If you find nothing, record a gap.
10. Mark each gap as fixed or outstanding. A fixed gap is one that the model already resolves in another place. An outstanding gap needs a change.
11. Report each outstanding gap as a finding in the format of K10. Ask the person which fixes to apply (K10).
12. For each confirmed fix, write a request (K8) on the element, concerning the part that must change.

## Rules

1. Do not flag a technical field as missing business data. An identifier that links steps is the exception, because K2 covers it.
2. Apply K2 to generated values as well as copied values. Distinguish input on a screen, context on a command, identifiers created with a fact, and read model calculations. An automation label is not an unexplained source.
3. A changing total or count belongs to a read model (K2 rule 16). A value fixed at decision time follows K1. Do not invent either an event field or a projection rule to settle an unknown.
4. One element used in two places is one element. Its fields are not duplicates.
5. Report a gap once, at the first element where the data goes missing (K10 rules 13, 14).
6. A field with a "starts here" origin where an upstream element supplies the value is a gap (K2 rules 5, 6).

Read `references/examples.md` when you need a sample gap table.

## Result

This skill writes nothing in the model during the audit. After the person confirms fixes, it writes requests (K8) on the elements concerned. A gap that the person accepts as debt becomes a decision under K10.

It reports to the person the chapters and the number of fields audited, and one table with one line for each gap: the element, the field, the kind of gap (no origin or no consumer), what the search found, and the status (fixed or outstanding). Then the findings and one verdict (K10).

## Done when

1. The report names every chapter of the model and the number of fields audited.
2. Every command field reaches an event, or a gap names it.
3. Every read model field has a source event or a computation, or a gap names it.
4. Every gap shows the search for the data elsewhere.
5. Every gap is marked fixed or outstanding, and appears once.
6. The report ends with one verdict.
7. The flow of the model is unchanged. The only new records are requests and debt decisions that the person confirmed.
