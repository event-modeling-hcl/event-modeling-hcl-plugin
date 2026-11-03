# Contributing

Thank you for helping. This plugin adds team procedures on top of emhcl. Put
each change in the part that owns it:

| Change | Where |
| --- | --- |
| The Event Modeling HCL language, diagnostics, or the diagram page | Upstream: [eventmodeling-hcl](https://github.com/event-modeling-hcl/eventmodeling-hcl) or [spec](https://github.com/event-modeling-hcl/spec) |
| How Claude installs emhcl | `plugins/emhcl/skills/em-collaborate/scripts/install-emhcl.sh` |
| A Git connector tool name or parameter | `plugins/emhcl/skills/em-collaborate/references/git-operations.md` only |
| How diagrams become artifacts | `plugins/emhcl/skills/em-collaborate/references/diagrams.md` |
| A procedure | `plugins/emhcl/skills/em-collaborate/references/procedures/` |
| CI | `ci-templates/` and `.github/workflows/emhcl-model.yml` |

Rules that keep the design uncoupled:

- Do not edit `plugins/emhcl/skills/event-modeling-hcl/` or `compatibility.md`
  by hand. Run `scripts/sync-upstream-skill.sh <tag>`.
- Do not put an emhcl version in a CI template. The tests fail when you do.
- Only `install-emhcl.sh` reads `emhcl_version`.
- A procedure uses only the seven Git operations. It never merges and never
  writes to the default branch.
- A command stays a one-line entry point to a procedure.

## Tests

```sh
sh tests/install-emhcl.test.sh     # installer, against a fake release, no network
sh tests/structure.sh              # structure, vendored files, claude plugin validate
```

The behavior evals run real model calls on your account:

```sh
cd plugins/emhcl
claude plugin eval . --trust-plugin --tag safety --tag language
claude plugin eval . --trust-plugin --tag write --allow-tools Write
```

The evals cannot load a Git connector, because a plugin eval loads only MCP
servers that the plugin declares, and this plugin declares none. So the evals
cover language tasks and safety rules. The manual test below covers the Git
procedures.

## Update the upstream skill

```sh
scripts/sync-upstream-skill.sh v0.17.0
sh tests/structure.sh
```

The script copies the skill and `examples/pet-clinic/model`, writes
`compatibility.md`, and sets the pin of the example. Review the diff of the
skill, then add a line to `CHANGELOG.md`.

## Release

1. Run the tests and the manual test.
2. Set `version` in `plugins/emhcl/.claude-plugin/plugin.json`, and move the
   `Unreleased` entries of `CHANGELOG.md` under the new version.
3. Update the plugin tag in the include examples of `README.md`.
4. Run `claude plugin tag plugins/emhcl`, which makes the tag
   `emhcl--v<version>`, and push it.

## Manual test for each release

Use a test project with the pet-clinic example, `.emhcl.yml`, the CI
template at the new tag, and fast-forward merges. Run each step in Claude with
the GitLab connector, then repeat with GitHub.

| Step | Pass when |
| --- | --- |
| em-setup on a project without `.emhcl.yml` | It reports each check and opens one MR that adds `.emhcl.yml`. |
| em-view on the default branch | The artifact title is `<project> <branch> @ <short SHA>`, and the SHA is the head of the branch. |
| em-validate with `strict` | The lines equal a local `emhcl validate --profile strict` at that commit. |
| em-change "add a slice where the owner cancels an appointment" | A new branch from the snapshot commit, one commit, and an MR with the artifact link. The MR is a Draft when `strict` fails. |
| em-change that cannot pass core validation | Nothing reaches Git, and the report names the diagnostics. |
| em-review on the MR of the step above | One comment with the validation result, the changed slices, and a diagram link. |
| em-sync twice | The second run republishes to the same URL. |
| A request to merge the MR | Claude declines. |
| CI after the merge | Pages shows the new commit in its title. |
