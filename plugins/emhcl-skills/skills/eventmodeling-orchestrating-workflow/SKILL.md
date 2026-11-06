---
name: eventmodeling-orchestrating-workflow
description: Runs a full event modeling run over the gates of the method contract. It finds the first gate that fails, names the model part that must change and the elements that fail, loads the skill that writes that part, and repeats until every gate passes or a stop rule applies. Use it when someone asks to build a complete event model from a domain description, documents, or a code base, to continue an unfinished model, or to find out what the model still needs. Writes no model part itself. Does not run a live session with a group of people.
metadata:
  version: "1.0.0"
  contract: "K0 K9 K12 H0 H3"
---

# Orchestrating a modeling run

This skill runs a modeling run over the gates of K12. Each pass finds the first gate that fails, names the part that must change, and loads the skill whose description says that it writes that part. The skill holds no modeling rule and no list of skills. It writes nothing in the model.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read the model if it exists, the sources (a domain description, documents, or code), and the goal of the person.

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`. The gates close in the order of H3, and each gate needs the validation of H0.

If the domain, the goal, or the limits are unclear, ask under K9 first: what the person models, which sources exist, what the result is for, and which limits apply. Then state your understanding in one sentence and ask the person to agree. In autonomous mode, state it and go on.

## Procedure

1. If the sources include documents or code that the model does not hold as evidence sources yet, load the skill whose description says that it takes facts from that kind of source. Do this before the first gate.
2. Read the gate state. Read the model. In an `.em.hcl` model, run `emhcl validate --profile workshop <model>`.
3. Test the gates in order. A gate fails when its test in K12 fails, when an open request on its part exists, or when the model is not valid.
4. Find the first gate that fails. Each gate before it passes, so its needs pass.
5. Tell the person in one line: the gate, the part, and the elements that fail it.
6. Load the skill whose description says that it writes that part. Give it the failing elements, the open requests on the part, and the sources. Never write the part yourself.
7. When that skill reports done, go back to step 2. Never load the writer of a part whose gate passes.
8. When the first failing gate is the reviews gate, load each skill whose description says that it reviews the model and writes nothing. Each fix that the person confirms becomes a request on its part. That request makes an earlier gate fail again, and the loop returns to it.
9. Stop when a stop rule below applies.
10. If the person wants a forecast after the ownership gate, load the skill whose description says that it estimates delivery time.
11. Write the final report. Use the result section below.

## Gate state in an .em.hcl model

Test the gates in this order (H3). Each line names what to read.

| Gate | It passes when |
| --- | --- |
| roles | Each person and each system that the sources name is an `actor`, a `system`, or a `team`. |
| events | Each business process of the sources has its `event` blocks. |
| streams | Each internal event has `aggregate`, and each aggregate has `identity`. |
| lifecycle states | Each aggregate has a `lifecycle` with its `state` blocks and end states. |
| screens | Each human `actor` is the `actor` of at least one `screen`. |
| commands | Each screen action and each trigger inside the system has a `command`. |
| lifecycle moves | Each command on a stream is in a `transition` or an `invalid_transition`. |
| automations | Each `automation` has a todo `readmodel` with `to = [processor.<id>]`. Each external event is read by an `automation`. |
| external mappings | Each translation `automation` has a `field_source` for each field of its command. |
| read models | Each screen field that shows data has a `readmodel` that feeds the screen. |
| chapters | Each workflow is in one `chapter`. |
| story order | Each workflow of the story is in `board { workflows = [...] }`. |
| command scenarios | Each `state_change` and each `automation` has a `scenario` for each case that the business supports. |
| read model scenarios | Each `readmodel` is the `then` target of at least one `scenario`. |
| reviews | No review finding is open. Each one is fixed or is a `decision` with `kind = "accepted_debt"`. |
| slice status | Each workflow has `status`. |
| ownership | Each workflow and each internal `bounded_context` has `owner`. |
| chapter summaries | Each complete `chapter` has a `description`. |

An open `hotspot` with `kind = "request"` fails the gate of the part that its `concerns` names.

## Stop rules

1. Every gate passes.
2. The review loop stops under K12: a review finds nothing new, or the person accepts each open finding as debt.
3. The same gate fails twice with the same failing elements after its writer ran. Stop and ask the person how to go on.
4. The writer of a part stops with an error that it cannot repair (H0). Stop and report the error.
5. The person says to stop.

## Large sources in layers

A large source runs in layers (K12).

1. In layer 0, run the gates up to chapters for the whole source, with business milestones only. Add no fields, scenarios, or screens.
2. Report the chapters to the person. Ask which chapter to detail first. Never pick it for the person. In autonomous mode, take the first chapter of the story and label the choice as assumed.
3. In each later pass, run the gates for the chosen chapter only. Model the whole story of that chapter, not only its first part.
4. Layer 1 adds the main flow, the key fields, and the main rules. Layer 2 and deeper add other paths, automations, the full field set, and error rules.
5. After each pass, ask: next chapter, deeper here, or stop.
6. A chapter that the person does not choose stays at layer 0.

In an `.em.hcl` model, layer 0 holds events and lifecycle states only (H3). The chapters of layer 0 stay in your report until their workflows exist.

## Rules

1. A correct model is the goal. If a gate needs more elements or more work than expected, do the work.
2. Never remove a required automation, read model, or translation step to keep the model small.
3. Never call a missing element accepted debt when the rule gives no exception. If a real trade of scope exists, tell the person and let the person decide.
4. Apply no modeling rule yourself. The writer of each part applies its rules.
5. Keep no working file beside the model. The model and your report hold every fact.

Read `references/examples.md` when you need a worked run.

## Result

This skill writes nothing in the model. After each pass, it tells the person the gate, the result, the part that changed, and the open questions. The final report lists each gate with pass or fail, the stop rule that ended the run, the open questions, the accepted debt, and each fact that the model cannot hold.

## Done when

1. The report names each gate in order with pass or fail, and the first failing gate with its part and its failing elements.
2. No writer of a part was loaded while an earlier gate failed.
3. This skill wrote nothing in the model. Each change came from the skill that writes that part.
4. The run ended on a stop rule, and the report names it.
5. Each review finding is fixed or accepted as debt, or the report names the open ones.
6. In an `.em.hcl` model, the last `emhcl validate --profile workshop` shows no core error.
