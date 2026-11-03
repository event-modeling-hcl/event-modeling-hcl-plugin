# em-view

Shows one branch of the model as a diagram, and answers questions about it.

Composition: C(DP3 snapshot → DP1 validate with `draft_profile` → DP4 publish).

Writes to Git: nothing.

## Input

The repository, and a branch. Without a branch, use the default branch. A
question about the model is optional.

## Steps

1. Do S1, S2, and S3 for the branch.
2. Do S4. Then do S5 with `draft_profile`. Keep the result for the report.
   A model with core errors can still render. Say which errors it has.
3. Publish a diagram as [../diagrams.md](../diagrams.md) says, with the title
   for em-view and no artifact URL. Do not republish the team artifact; that
   is em-sync.
4. Answer the question of the person from the snapshot files. Load the
   `event-modeling-hcl` skill for the meaning of the blocks. Name the
   workflow, the file, and the line of each element that you mention. When
   the person asks about a flow, follow the `to` and `from` edges in the files.
   Do not guess beyond the files.

If the person then asks for a change, run em-change. If the snapshot is not
the default branch, say that em-change starts from the default branch.

## Report

The header block with `Procedure: em-view`, the branch, the commit, one `Ran:`
line, and `Artifact:`. Name `canonical_url` as the canonical view when it is
set. Then the answer.
