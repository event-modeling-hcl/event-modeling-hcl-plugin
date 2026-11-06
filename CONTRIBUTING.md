# Contributing

Thank you for helping. This repository holds two plugins: `emhcl`, which adds
team procedures on top of emhcl, and `emhcl-skills`, the home of the emhcl
agent skills. Put each change in the part that owns it:

| Change | Where |
| --- | --- |
| The Event Modeling HCL language, diagnostics, or the diagram page | Upstream: [eventmodeling-hcl](https://github.com/event-modeling-hcl/eventmodeling-hcl) or [spec](https://github.com/event-modeling-hcl/spec) |
| How agents write, repair, and validate `.em.hcl` | `plugins/emhcl-skills/skills/event-modeling-hcl/` |
| A rule that more than one method skill uses | `contract/method.md`, or `contract/hcl-binding.md` for its encoding. Then run `scripts/build-contract.sh`. |
| One step of the method | `plugins/emhcl-skills/skills/eventmodeling-<step>/` and its three evals in `plugins/emhcl-skills/evals/` |
| How Claude installs emhcl | `plugins/emhcl/skills/em-collaborate/scripts/install-emhcl.sh` |
| A Git connector tool name or parameter | `plugins/emhcl/skills/em-collaborate/references/git-operations.md` only |
| How diagrams become artifacts | `plugins/emhcl/skills/em-collaborate/references/diagrams.md` |
| A procedure | `plugins/emhcl/skills/em-collaborate/references/procedures/` |
| CI | `ci-templates/` and `.github/workflows/emhcl-model.yml` |

Rules that keep the design uncoupled:

- Do not edit `compatibility.md` or a `references/contract.md` by hand. Run
  `scripts/sync-upstream.sh <tag>` or `scripts/build-contract.sh`.
- A method skill never names another skill, and never restates a rule of the
  contract. It writes only its own part of the model and sends other changes
  as request records. The structure tests fail when a skill names another
  skill.
- A change to the language skill `event-modeling-hcl` that follows a new
  emhcl release changes `metadata.spec_version` and `metadata.emhcl_min` in
  its front matter. Then run `scripts/sync-upstream.sh <tag>`.
- Do not put an emhcl version in a CI template. The tests fail when you do.
- Only `install-emhcl.sh` reads `emhcl_version`.
- A procedure uses only the seven Git operations. It never merges and never
  writes to the default branch.
- A command stays a one-line entry point to a procedure.

## Tests

```sh
sh tests/install-emhcl.test.sh     # installer, against a fake release, no network
sh tests/structure.sh              # structure, contract copies, skill names, example, claude plugin validate
sh scripts/check-source-overlap.sh # text shared with the source skills of unknown license
```

The behavior evals run real model calls on your account:

Run `claude auth status` first. If the CLI reports that you are not logged
in, authenticate before running the evals. The structure suite parses every
eval prompt and grader without a model call. Parsing does not establish that
a skill gives the expected answer.

```sh
cd plugins/emhcl
claude plugin eval . --trust-plugin --tag safety --tag language
cd ../emhcl-skills
claude plugin eval . --trust-plugin --tag method
claude plugin eval . --trust-plugin --tag write --allow-tools Write
```

The evals cannot load a Git connector, because a plugin eval loads only MCP
servers that the plugin declares, and `emhcl` declares none. So the evals
cover language tasks, method skills, and safety rules. The manual test below
covers the Git procedures. An eval of a plugin path loads only that plugin, so
the evals of `event-modeling-hcl` and the method skills live in
`emhcl-skills`.

## Update to a new emhcl release

```sh
UPSTREAM_REPO=<local eventmodeling-hcl clone> scripts/sync-upstream.sh v0.17.0
sh tests/structure.sh
```

The script copies `examples/pet-clinic/model` at the tag, writes
`compatibility.md` from the front matter of `event-modeling-hcl`, and sets the
pin of the example. With `EMHCL=<binary>`, `--check` also compares the
`spec_version` of the skill with the binary. Add a line to `CHANGELOG.md`.

## Release

Do not release the new method content until the source-license question in
`contract/CREDITS.md` is resolved. The text-overlap scan cannot grant rights
to use source material.

1. Run the tests and the manual test.
2. Set `version` in the `plugin.json` of each changed plugin, and move the
   `Unreleased` entries of `CHANGELOG.md` under the new version.
3. Update the plugin tag in the include examples of `README.md`.
4. Run `claude plugin tag plugins/emhcl` and `claude plugin tag
   plugins/emhcl-skills`, which make the tags `emhcl--v<version>` and
   `emhcl-skills--v<version>`, and push them.

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
