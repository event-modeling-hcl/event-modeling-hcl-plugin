# em-setup

Makes sure that each part of the plugin has its inputs for one repository.
Proposes `.emhcl.yml` through an MR when the file is missing.

Composition: S(DP3 tools present, DP1 install, DP2 range, `.emhcl.yml` read),
then C(DP3 commit-branch → DP3 open-mr) only for a missing file.

Writes to Git: only a new branch and an MR, and only when `.emhcl.yml` is
missing.

## Input

The repository. A branch is not needed; em-setup checks the default branch.

## Checks

The four checks need no order. Run each one, and report each result as `ok`,
`warning`, or `missing`, with one sentence.

1. Connector tools (DP3). Do S1. Then check that each tool of the binding in
   [../git-operations.md](../git-operations.md) is available for the host.
   - GitLab: `add_commit` must accept `start_sha`. If its schema has no
     `start_sha`, the GitLab instance is older than 19.4. em-change cannot
     write then. Tell the person to ask the GitLab administrators for an
     upgrade. Call `get_mcp_server_version` and report the version.
   - GitHub: report that the GitHub binding checks the default branch again
     before each commit, because it cannot start a branch at a commit.
2. Configuration. Do S2 and S3 on the default branch. Report each key of
   `.emhcl.yml`, its value, and each key that is unknown or absent. Report the
   number of model files, and each subfolder of `model_path` that holds
   `.em.hcl` files.
3. Validator (DP1). Do S4. Report the installed version.
4. Skill range (DP2). Report the result of `check-compatibility.sh` from S4.

Then validate once with S5 and the profile `valid`, and report the result in
one line. If the model reports `EM015` and has no `board` block, it is a
v0.4.0 model. Tell the person to run `emhcl migrate -w <model folder>` and to
propose the result with em-change.

## Propose a missing `.emhcl.yml`

Only when the file is missing:

1. Find the model folder. Call list-model on the repository root and on the
   folders that it lists, one level deep. Use the folder that holds the
   `.em.hcl` files. If several folders hold them, ask the person.
2. Write the file as "A proposed file" in
   [../configuration.md](../configuration.md) says.
3. Write it to a copy of the snapshot, and do S4 with it, so that the pin
   installs before you propose it.
4. commit-branch: one new file `.emhcl.yml`, branch name with the short name
   `add-emhcl-config`, commit message `Add .emhcl.yml for the emhcl plugin`.
5. open-mr: ready, not Draft. Title `Add .emhcl.yml for the emhcl plugin`.
   Description: the purpose of each key in one line each, and a line that
   says a reviewer merges it.

## CI and merge settings

These steps are for a person with maintainer rights. em-setup does not do
them. Give them as a list when CI is not set up yet.

- GitLab: add the include block from the README of the plugin to
  `.gitlab-ci.yml`, with the plugin tag in both places. Set the merge method
  of the project to "Fast-forward merge". Turn on "Pipelines must succeed".
- GitHub: call the reusable workflow `emhcl-model.yml` at the plugin tag.
  Turn on "Require linear history" and a required status check for
  `emhcl-validate` on the default branch.

## Report

The header block of the skill, with `Procedure: em-setup`, then one line for
each check, then the MR link if em-setup opened one.
