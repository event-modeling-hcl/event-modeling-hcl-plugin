---
name: eventmodeling-auditing-model-rules
description: Audits an event model against the rules for events, commands, read models, streams, lifecycles, slices, flow, and shapes, and gives one verdict of PASS, PASS WITH WARNINGS, or FAIL. Use it when someone asks to review, check, or validate a model, to find modeling mistakes, or to know if a model is ready. It also runs as a partial audit on an early model with only some parts. Writes nothing in the model until the person confirms a fix, then writes requests only. Does not audit field origins or scenario coverage.
metadata:
  version: "1.0.0"
  contract: "K0 K1 K3 K4 K7 K8 K9 K10 H0 H5 H10 H11"
---

# Auditing model rules

This skill gives one audit of the model: one numbered list of audits, two final questions, and one verdict. Each audit tests one contract rule against every element that it covers and reports evidence from the model. The skill writes nothing in the model during the audit. After the person confirms a fix, it writes requests only.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs: every part of the model that exists. Do not change anything during the audit (K10).

If the model is an `.em.hcl` file or folder:

1. Run `emhcl validate --profile strict <model>`.
2. Copy each output line unchanged into the report, under the heading "Validator".
3. Skip each audit below that is marked "HCL: validator". The validator already performs it. Write "covered by the validator" as its status.
4. Run the other audits as judgment audits.

## Procedure

1. Look at which parts exist. Run each audit whose inputs exist. For each audit whose input is missing, write NOT RUN and name the missing part. Never mark such an audit PASS.
2. If at least one audit is NOT RUN, the run is partial. Say so at the top of the report.
3. Run the audits in order. Run each audit once. A later audit never repeats the test of an earlier one.
4. For each audit, write its number, a status of PASS, WARN, or FAIL, and the evidence. Evidence names the real elements in the model. A count alone is never evidence.
5. Answer the two final questions.
6. Give the verdict.
7. Report each finding in the format of K10. Ask the person which fixes to apply (K10).
8. For each confirmed fix, write a request (K8) on the element, concerning the part that must change.

### Audits

Each audit names its rule and its inputs.

Events (inputs: events)

- 1.1 Each event is a fact that happened, not a calculation. K1 rules 3, 19 to 21, 35.
- 1.2 Each event name is in the past tense and states a fact, not a possibility or a waiting state. K1 rules 1, 36, 37.
- 1.3 No event records a user interface action or machinery. K1 rules 33, 34.
- 1.4 No two events mean the same thing. One element used in two places is one element. K1 rule 14.

Streams and lifecycles (inputs: events, streams, lifecycles)

- 2.1 Each event belongs to exactly one stream. K0 (streams). An event that seems to belong to two streams shows a naming or boundary mistake.
- 2.2 Each stream has one lifecycle with one start move, and each path reaches an end state or returns to a named state. K7 rules 3, 5, 8. HCL: validator for the form of the lifecycle (EM017). The path test stays a judgment audit.
- 2.3 Each failure is an event only when the business records it. K7 rule 10.

Commands (inputs: commands, screens or automations, roles)

- 3.1 Each command has exactly one issuer, a screen or an automation. K1 rule 16. Two issuers is a FAIL.
- 3.2 Each command names a specific role or system actor. K1 rule 17. A generic "User" is a FAIL. With no roles in the model, this audit is NOT RUN.
- 3.3 Each command states its preconditions and produces events or states how it rejects. K1 rules 6, 7. A rule that "everyone knows" is a WARN until the model states it.
- 3.4 No command only loads data. K1 rule 32.
- 3.5 No read model drives the decision of a command. K1 rule 10.

Read models (inputs: read models)

- 4.1 Each read model is built only from events, answers one query, and serves a screen or an automation. K1 rules 8, 11.
- 4.2 No read model name names machinery. K1 rule 9.

Slices and flow (inputs: slices)

- 5.1 Apply K3 rules 4 to 6 to each slice. A state-change slice covers one command, a state-view slice covers one read model, and an automation slice covers one automation with its supporting command and todo list. Report combined independent responsibilities. This is a method audit, not a guarantee from the HCL validator.
- 5.2 Each move between slices is an allowed transition, and no flow starts with an untriggered state change. K3 rules 14 to 18. HCL: validator for the edges of each workflow. The order of workflows on the board stays a judgment audit.
- 5.3 The timeline reads forward. Each upstream element comes before its consumers. K3 rules 19, 20.
- 5.4 Alternative paths exist where the business needs them: cancel, failure, and compensation. K7 rule 2.
- 5.5 Apply the pending-work and translation rules of K3. Include internal cross-team boundaries, worker completion, translation projections, and any explicit minimal-encoding omission. A CLI classification alone does not prove business meaning.

Shapes (inputs: screens, commands, read models, scenarios)

- 6.1 Judge each shape under K4. A bed is always a finding. The other shapes become findings only after the judgment of K4. HCL: the validator signals EM401 to EM403 and EM405 are counts only. Judge each signal here.

### Final questions

1. Can a modeler unfamiliar with the domain understand this model within 15 minutes?
2. Can the rule behind a read model change without rewriting recorded business facts? This question does not require Event Sourcing.

Answer each with yes or no and one reason. On a partial run, answer "not asked" when the parts that a question needs do not exist.

## Rules

1. The verdict follows K10, with these additions. Any FAIL, or any validator error, gives FAIL. A final question answered no gives at most PASS WITH WARNINGS.
2. A partial run gives a verdict for the audits that ran only. The report says so.
3. Each FAIL names the element, the contract rule id, and a proposed fix.
4. Your own findings never carry an EM code. Only copied validator lines do (H0).

Read `references/examples.md` when you need a sample report.

## Result

This skill writes nothing in the model during the audit. After the person confirms fixes, it writes requests (K8) on the elements concerned.

It reports to the person: the validator lines when the model is HCL, one line for each audit, the answers to the final questions, and one verdict.

## Done when

1. Every audit has a status and evidence, NOT RUN with the missing part, or "covered by the validator".
2. No rule is tested twice.
3. Every FAIL names an element, a contract rule id, and a fix.
4. Both final questions have an answer and a reason, or "not asked" on a partial run.
5. The report ends with one verdict of PASS, PASS WITH WARNINGS, or FAIL.
6. The flow of the model is unchanged. The only new records are requests for confirmed fixes.
