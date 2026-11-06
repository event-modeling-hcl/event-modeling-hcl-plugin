---
name: eventmodeling-orchestrating-workflow
description: Runs a full event modeling run over the gates of the method contract. It finds the first gate that fails, names the model part that must change and the elements that fail, loads the skill that writes that part, and repeats until every gate passes or a stop rule applies. Use it when someone asks to build a complete event model from a domain description, documents, or a code base, to continue an unfinished model, or to find out what the model still needs. Writes no model part itself. Does not run a live session with a group of people.
metadata:
  version: "1.0.0"
  contract: "K0 K9 K12 H0 H3 H10"
---

# Orchestrating a modeling run

This skill applies the gates of K12. It finds the first failing gate, names the missing part, and loads the writer whose description owns that part. Explicit requests route prerequisite work to its writer. The coordinator writes no model part and holds no separate rule or skill list.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Read the model if it exists, the sources (a domain description, documents, or code), and the goal of the person.

If the model is an `.em.hcl` file or folder, follow H0 and the gate order of H3. Use K12 for gate criteria and prerequisite requests. Reuse the language authority for legal syntax and diagnostics.

If the domain, the goal, or the limits are unclear, ask under K9 first: what the person models, which sources exist, what the result is for, and which limits apply. Then state your understanding in one sentence and ask the person to agree. In autonomous mode, state it and go on.

## Procedure

1. If the sources include documents or code that the model does not hold as evidence sources yet, load the skill whose description says that it takes facts from that kind of source. Do this before the first gate.
2. Read the gate state. Read the model. In an `.em.hcl` model, run `emhcl validate --profile workshop <model>`.
3. Test gates in their canonical order. Apply K12 to open requests, incomplete models, and validity. Report future-part diagnostics without claiming that an incomplete model passes.
4. Find the first failing gate and its missing part. An explicit prerequisite request can require its own writer before that gate passes.
5. Tell the person in one line: the gate, the part, and the elements that fail it.
6. Load the writer of the missing part. Supply failing elements, sources, open requests, and K13 permissions. If an explicit request needs another part first, dispatch that request to its writer and then return. Never write either part yourself.
7. After the writer returns, retest the blocked gate or request. Apply the repeated-failure and request-cycle stop rules of K12. Otherwise return to step 2.
8. At the reviews gate, load each skill whose description says that it reviews the model and writes nothing. Each approved fix becomes a request on its part and reopens that gate. When reviews converge under K12, close only the reviews gate. Continue to slice status, ownership, and chapter summaries.
9. Stop when a stop rule below applies.
10. If the person wants a forecast after the ownership gate, load the skill whose description says that it estimates delivery time.
11. Write the final report. Use the result section below.

## Gate state in an .em.hcl model

Read H3 for the gate order and K12 for their criteria. Use the relevant H section to locate each method fact. Do not maintain a second gate table here.

Open requests identify their part through H10. A missing command, event, or other prerequisite goes to that part's writer. Preserve valid intermediate artifacts. Record unresolved needs rather than inventing syntax, references, or elements to silence a diagnostic.

## Stop rules

1. Every gate passes.
2. A gate or prerequisite request reaches the repeated-failure limit of K12, or unresolved requests form a cycle. Report the failing elements and requests.
3. A writer stops with a language error that it cannot repair, a missing material business decision, or permission blocked under K13. Report the blocker without changing scope or another part.
4. The person says to stop.

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
2. Writers ran only for a failing gate or its explicit prerequisite request. The report names any prerequisite dispatch and its result.
3. This skill wrote nothing in the model. Each change came from the skill that writes that part.
4. The run ended on a stop rule, and the report names it.
5. Each review finding is fixed or accepted as debt, or the report names the open ones.
6. In a completed HCL run, workshop validation has no core error. In a blocked or incomplete run, the report preserves the outstanding diagnostics and their prerequisite requests.
