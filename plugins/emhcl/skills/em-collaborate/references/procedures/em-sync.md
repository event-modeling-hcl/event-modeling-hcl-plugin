# em-sync

Republishes the team artifact from the default branch.

Composition: C(DP3 snapshot of the default branch → DP4 republish to
`team_artifact_url`).

Writes to Git: nothing.

## Input

The repository. em-sync always uses the default branch.

## Steps

1. Do S1, S2, and S3 for the default branch. If the repository has no
   `.emhcl.yml`, stop and suggest em-setup.
2. Do S4. Then do S5 with `merge_profile`, so that the report says whether
   the default branch still passes the CI gate.
3. Publish a diagram as [../diagrams.md](../diagrams.md) says, with the
   em-sync title.
   - When `team_artifact_url` is set, publish as a new version of that
     artifact. If the publish fails because the person cannot edit the
     artifact, say that the person needs "Can edit" access from the owner of
     the artifact. Do not make a new artifact in its place.
   - When `team_artifact_url` is empty, publish a new artifact. Then tell the
     person to share it with everyone at the organization, and to give "Can
     edit" access to the people who run em-sync. Give the line
     `team_artifact_url: "<URL>"` and say that a maintainer adds it to
     `.emhcl.yml` with a normal MR. em-sync does not write to Git.

## Report

The header block with `Procedure: em-sync`, the default branch, the commit,
the `Ran:` line, and `Artifact:`. Name `canonical_url` as the canonical view
when it is set, and say that the team artifact mirrors it.
