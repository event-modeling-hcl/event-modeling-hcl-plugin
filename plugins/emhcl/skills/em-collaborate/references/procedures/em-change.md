# em-change

Turns a request in plain words into model edits, validates them, publishes a
diagram, and opens an MR.

Composition: C(DP3 snapshot → DP2 edit and repair → DP4 proposal artifact →
DP3 commit-branch → DP3 open-mr).

Writes to Git: one new branch and one MR. Never the default branch.

## Input

The repository and the change in plain words. A change always starts from the
default branch.

## Order

The five steps depend on each other, so run them in this order: E1, E2, E3,
E4, E5. Do not start a step before the step before it is done.

### E1. Snapshot

Do S1, S2, and S3 for the default branch. Call its commit S. Do S4. If the
repository has no `.emhcl.yml`, stop and suggest em-setup.

Copy `<work>/S/` to `<work>/change-S/`. Edit only the copy.

### E2. Edit and repair

1. Load the `event-modeling-hcl` skill and follow it. Respect its rules about
   workflow `status`, global IDs in a folder model, the board, and the shape
   of the model. Keep the existing file layout. Put a new workflow in a new
   file only when each workflow already has its own file.
2. If the request leaves a business decision open, ask one focused question,
   or record an open `hotspot` as the skill says. Do not invent the rule.
3. Run `"$EMHCL" fmt -w <file>` on each file that you created or changed. Do
   not format other files, so that the MR shows only your change.
4. Validate the copy with S5 and the profile `valid`. While
   `has_core_errors` is true, repair and validate again. Use the circuit
   breaker of the `event-modeling-hcl` skill: after two failed repairs of one
   code on one element, stop editing for that code.
5. If the breaker opened, stop here. Write nothing to Git. Report each
   remaining diagnostic and the two attempts.
6. Validate the copy with S5 and `merge_profile`. If `has_errors` is true,
   the MR will be a Draft. Keep the diagnostics for the description.
7. Compare the snapshot with the copy:

   ```sh
   "$EMHCL" diff <work>/S/<model_path> <work>/change-S/<model_path>
   ```

   Keep its lines. Find the changed files with
   `diff -rq <work>/S <work>/change-S`. If nothing changed, stop and say so.

### E3. Proposal artifact

Choose the branch name as in commit-branch of
[../git-operations.md](../git-operations.md). Publish a diagram of the copy as
[../diagrams.md](../diagrams.md) says, with the em-change title and no
artifact URL. If it cannot publish, continue without a link.

### E4. Branch and commit

commit-branch with S, the branch name, the commit message
`model: <short summary of the change>`, and all changed files. With GitHub,
this step checks first that the default branch is still at S.

If commit-branch fails, stop. Report the error. The artifact stays private to
the author.

### E5. Merge request

open-mr from the new branch to the default branch. It is a Draft when the
copy failed `merge_profile` in E2. The title is the summary of the change,
in fewer than 72 characters.

Write the description in this form. No line starts with `/`.

```text
<The request of the person, in one or two plain sentences.>

Changes (emhcl diff):
<the lines of emhcl diff, in a code block>

Validation with emhcl <version>, profile <merge_profile>: <passes, or fails with
the counts of each code>.
<When it fails: the lines that emhcl printed, in a code block, and one sentence
that says what a person must decide before the MR can leave Draft.>

Diagram: <artifact URL>. Open it and ask the author for access if it does not open.
<Or: No diagram link exists: <reason>.>

Base commit: <S>
Review: <reviewers_hint>

Opened by the emhcl plugin for Claude (em-change). A reviewer merges this MR after CI passes.
```

If open-mr fails, report the branch name and the error. Repeat only E5 when
the person asks.

## Report

The header block with `Procedure: em-change`, the default branch, commit S,
the `Ran:` lines, `Artifact:`, and `MR:` with `(Draft)` when it is a Draft.
Then the share steps from [../diagrams.md](../diagrams.md), and the open
questions, if any.
