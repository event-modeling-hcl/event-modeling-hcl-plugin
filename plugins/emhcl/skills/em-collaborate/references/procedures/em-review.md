# em-review

Validates the head of an MR, lists the changed slices, publishes a diagram,
and posts one comment.

Composition: C(DP3 read-mr and snapshots → DP1 validate the head with
`merge_profile` → slice comparison → DP4 publish → DP3 comment-mr).

Writes to Git: one comment on the MR.

## Input

An MR number or URL, and the repository when the number alone does not name
it.

## Steps

1. Do S1. Then read-mr. Keep the source branch, the target branch, the base
   commit B, the head commit H, and the changed files. If no changed file is
   `.emhcl.yml` or a file in `model_path`, say that the MR does not change the
   model, and stop without a comment.
2. Do S2 and S3 for H. Then do S3 for B, with the `model_path` of H. Skip
   resolve-ref in both, because read-mr gave both commits.
3. Do S4 with the `.emhcl.yml` of H, because CI uses the configuration of the
   MR. Then do S5 on H with `merge_profile`. Run it again without
   `--format json` to copy the lines.
4. Compare the slices:

   ```sh
   "$EMHCL" diff --format json <work>/B/<model_path> <work>/H/<model_path>
   ```

   Each top-level entry with `kind` `workflow` is a slice that the MR added,
   removed, or changed. Other top-level entries are catalog changes, for
   example an event or a bounded context. emhcl compares the typed models, so
   a block that only moved to another file or changed its layout gives no
   entry. If the base model has a core error, diff exits 1; then list the
   changed files instead, and say why.
5. Load the `event-modeling-hcl` skill. Read each changed slice in H. Write
   your own findings as `Review:` lines, as that skill describes. Keep them
   apart from the lines that emhcl printed.
6. Publish a diagram of H as [../diagrams.md](../diagrams.md) says, with the
   em-review title and no artifact URL.
7. comment-mr with one comment in the form below. Before you post, show the
   comment to the person when they asked only for a review in chat, and post
   when they agree. When they ran em-review as a command, post it.

```text
emhcl review of <short H> (base <short B>)

Validation with emhcl <version>, profile <merge_profile>: <passes, or fails with
the counts of each code>.
<When it fails: the lines that emhcl printed, in a code block.>

Slices:
- added: <workflow IDs, or none>
- removed: <workflow IDs, or none>
- changed: <workflow IDs, or none>
- catalog: <other declarations, or none>

Review notes:
<the Review: lines, or "none">

Diagram: <artifact URL>. <Or: No diagram link exists: <reason>.>

Posted by the emhcl plugin for Claude (em-review). CI decides whether the MR can merge.
```

No line of the comment starts with `/`.

## Report

The header block with `Procedure: em-review`, the source branch, commit H,
the `Ran:` lines, `Artifact:`, and `MR:`. Then the slice list.
