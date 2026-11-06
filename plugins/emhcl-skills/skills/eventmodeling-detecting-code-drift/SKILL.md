---
name: eventmodeling-detecting-code-drift
description: Finds each code change since the last analyzed commit that the model does not show, and proposes a fix for each. Drift goes one way only, the code changed and the model did not. Each confirmed fix becomes a request on the element, and the new baseline is recorded only when every finding is handled. Use it when someone asks whether the model is still up to date with the code, what changed in the code since the model was made, or to sync the model after hand edits to generated code. Does not write events, commands, screens, read models, scenarios, or any other model part. Does not edit code. Does not collect first evidence from code that the model never analyzed.
metadata:
  version: "1.0.0"
  contract: "K0 K8 K9 K10 H0 H10"
---

# Detecting code drift

Drift is a code change that the model does not show. This skill reads the commits since the baseline, one at a time, and reports each behavior change that the model misses, with a proposed fix. It writes records only: a request for each confirmed fix, a decision for each declined or accepted finding, and, at the end, one evidence source of the kind code for the pass. It writes no element of any model part.

## Before you start

Read `references/contract.md`. It holds the rules that this skill follows.

Inputs:

- the code and its git history. If there is no git history, say so in one line and stop.
- the baseline of each chapter in scope: its latest evidence source of the kind code (K8 rule 24). Its location holds the commit, and its description holds the scope.
- the decisions and accepted debt of the chapter, which name intended differences
- the evidence on the elements of the chapter, which maps code locations to elements

If the model is an `.em.hcl` file or folder, follow the H sections of `references/contract.md`.

If the baseline is missing, or its commit is not in the history of this branch, ask once for a start commit (K9). Offer the newest commit that the model records for the chapter, or the last few commits. If the person gave a start commit up front, use it. Never compare the whole model with the whole code.

## Procedure

1. Resolve each open request from an earlier drift pass that concerns the records of this skill first.
2. Get the baseline for each chapter in scope. Chapters with the same baseline share one read of the history.
3. List the commits from the baseline to the current commit, oldest first. Add uncommitted changes when you read the current branch.
4. Walk the commits one at a time. Do not judge from the total difference alone. A total difference hides a later hand edit inside a file that an earlier commit created.
5. Sort each commit per file into behavior or noise. One commit can hold both kinds.
6. Treat a commit as generated only if a record says that it was generated from the model. Its files show the as-built state of that slice. Every later change to those files is a hand change.
7. If no behavior change remains, report that the code did not change in a way that affects the model. Then go to step 12.
8. Map each behavior change to an element. Use evidence locations first, then the chapter scope, then names in the code. If a change maps to no element, report it as a candidate new element and name its most likely chapter.
9. Read the model only for the elements that a change hit. Read the code as it is now for those elements.
10. Write each finding under K10 and the rules below.
11. Show the report and ask which fixes to apply (K10). Write each confirmed fix as a request (K8) on its element, concerning the part that must change. Write a decision for each declined finding and each finding accepted as debt.
12. When every finding is handled, write the evidence source for this pass under K8 rules 21 to 24. Its description names the declined findings.

## Rules

### Behavior and noise

Behavior files change what the system does: handlers, services, entities, events, projections, queries, schemas, migrations, input rules, screens, and tests. Noise files do not: dependency updates, build and CI settings, formatting, docs, tool settings, and generated files. List noise in the report footer as not relevant. Noise is never a finding.

### Finding kinds

| Kind | The code change | Part that the request concerns |
| --- | --- | --- |
| Fields | adds, removes, or renames a field, or changes its type, required state, or identity | the part of each element along the chain |
| Rules | adds, removes, or changes an input rule, guard, error case, default, or test | command scenarios or read model scenarios |
| Screens | changes what a screen shows or submits | screens |
| Connections | makes a handler, query, or automation use or produce something that the model does not connect | the part of the element that changes |
| Element | adds, removes, or renames a command, event, read model, or automation | that part |
| Slice | adds a whole feature, or removes a slice that the model marks as done | slice status, and the parts of the new elements |

Each finding names, beside the K10 parts, the kind, the commits, and the files with line numbers.

### Judging filters

- Only changes since the baseline count. Older differences are accepted, unless a newer change touched them.
- A change only on the model side is planned work. Never report it.
- Ignore a change that reduces a difference between the code and the model.
- Framework noise is not a finding: generated ids, envelope fields, logging, and refactorings that keep behavior.

### Fix direction

The code change is the newer decision. The default fix updates the model. Propose a code revert only when the change is clearly accidental, such as a typo, a debug leftover, or a disabled test, and say why. Never edit the code.

### Handled findings

A finding is handled when its request is written, when a request asks to set its slice back to planned, when the person declines it, or when the person accepts it as debt. If the person did not answer, write no evidence source. The next run reports the same changes again.

Read `references/examples.md` when you need a worked report.

## Result

The skill writes requests, decisions, and one evidence source of the kind code. It writes no element.

The report to the person is Markdown with one checkbox per finding:

- a heading with the scope
- the range from the baseline to the current commit, the number of commits, and the number of behavior files
- one section per finding kind, each finding as "- [ ]" with its proposed fix
- a short summary that names the most important fix
- the commits, one line each, with generated commits marked
- the noise files as not relevant

Leave out empty sections. If nothing drifted, say so in one line.

## Done when

1. The report lists the commits one at a time, oldest first, and no finding comes from a change on the model side only.
2. Each finding has a kind, commits, files with lines, an element, a severity, and a proposed fix that names the part it changes and every affected screen.
3. No request or decision exists for a finding that the person did not confirm, decline, or accept.
4. The new evidence source of the kind code exists only when every finding is handled, and it names the code root and the short commit.
5. No evidence source of an earlier pass changed.
