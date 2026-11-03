# em-validate

Validates one branch with a profile, and explains each diagnostic in plain
words.

Composition: C(DP3 snapshot → DP1 validate with the named profile, else
`draft_profile` → explain).

Writes to Git: nothing.

## Input

The repository, a branch, and a profile. Without a branch, use the default
branch. Without a profile, use `draft_profile`. To see what CI will say, the
person names `merge_profile` or asks whether the branch can merge.

## Steps

1. Do S1, S2, and S3 for the branch.
2. Do S4. Then run validate without `--format json`, so that you can copy the
   lines unchanged. Then run it with `--format json` to count the codes.
3. Load the `event-modeling-hcl` skill. For each diagnostic, explain in one or
   two plain sentences what is wrong, where it is, and what kind of change
   fixes it. Read the file at the line to name the element. Say whether the
   code is a core error, which blocks every MR, or a judgment code, whose
   severity the profile sets.
4. If the profile is not `merge_profile`, say in one line whether the model
   would also pass `merge_profile`. Run validate a third time for that.

Do not change files. If the person asks for a fix, run em-change.

## Report

The header block with `Procedure: em-validate`, the branch, the commit, and
the `Ran:` lines. Then the lines that emhcl printed, unchanged, in a code
block. Then your explanations, one short paragraph for each code, in the order
of the files.
