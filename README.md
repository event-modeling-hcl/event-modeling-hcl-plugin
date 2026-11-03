# emhcl plugin for Claude

An open-source Claude plugin for teams that keep an event model in
[Event Modeling HCL](https://github.com/event-modeling-hcl/spec) (`.em.hcl`)
files. Each person on a team can view, change, and review the model through
Claude. A change reaches the default branch only through a merge request in
GitLab or GitHub, which a person reviews and merges.

The plugin works in Claude chat, Cowork, and Claude Code. It uses the Apache-2.0
license, the same license as [emhcl](https://github.com/event-modeling-hcl/eventmodeling-hcl).

## What it does

| Command | What it does | Writes to Git |
| --- | --- | --- |
| `em-setup` | Checks the connector, the validator, and `.emhcl.yml`. Proposes `.emhcl.yml` through an MR when it is missing. | Only an MR |
| `em-view` | Shows a branch as a diagram and answers questions about it | No |
| `em-validate` | Validates a branch with a profile and explains each diagnostic in plain words | No |
| `em-change` | Turns a request in plain words into edits, validates them, publishes a diagram, and opens an MR | A new branch and an MR |
| `em-review` | Validates the head of an MR, lists the changed slices, and publishes a diagram | One comment |
| `em-sync` | Republishes the shared team artifact from the default branch | No |

In Cowork and Claude Code, run a command as `/emhcl:em-change`. In Claude chat,
ask in plain words; Claude uses the matching procedure. The plugin never merges
and never writes to the default branch.

## Install

Add the marketplace and install the plugin:

```sh
claude plugin marketplace add event-modeling-hcl/emhcl-plugin
claude plugin install emhcl@event-modeling-hcl
```

You also need one Git connector in Claude:

- GitLab: the official GitLab MCP server. em-change needs GitLab 19.4 or later,
  because it starts each branch at an exact commit.
- GitHub: the GitHub MCP server.

Then ask Claude to run em-setup for your repository.

## Set up a model repository

1. Keep the model in one folder. emhcl reads only the `.em.hcl` files directly
   in it, and it ignores subfolders. A model for specification v0.4.0 needs
   `emhcl migrate -w <folder>` first.
2. Add `.emhcl.yml` at the repository root. em-setup proposes it. See
   [examples/pet-clinic/.emhcl.yml](examples/pet-clinic/.emhcl.yml) and the
   [key reference](plugins/emhcl/skills/em-collaborate/references/configuration.md).
3. Add the CI jobs, and use fast-forward merges.

GitLab, in `.gitlab-ci.yml`:

```yaml
include:
  - remote: https://raw.githubusercontent.com/event-modeling-hcl/emhcl-plugin/emhcl--v0.1.0/ci-templates/emhcl.gitlab-ci.yml
    inputs:
      plugin_ref: emhcl--v0.1.0
```

Set the merge method to "Fast-forward merge" and turn on "Pipelines must
succeed". The job `emhcl-validate` validates with `merge_profile`, and the job
`pages` publishes the default branch to GitLab Pages.

GitHub, in `.github/workflows/model.yml`:

```yaml
on:
  pull_request:
  push:
    branches: [main]
jobs:
  model:
    uses: event-modeling-hcl/emhcl-plugin/.github/workflows/emhcl-model.yml@emhcl--v0.1.0
    with:
      plugin_ref: emhcl--v0.1.0
    permissions:
      contents: read
      pages: write
      id-token: write
```

Require the status check `model / emhcl-validate` and linear history on the
default branch.

The CI templates name no emhcl version. They run the same
`install-emhcl.sh` as Claude, and that script installs the release that
`.emhcl.yml` pins. So Claude and CI validate each commit with the same emhcl.

## How it is built

The design follows the plan in
[emhcl Plugin for Claude — Open-Source Plan.md](emhcl%20Plugin%20for%20Claude%20%E2%80%94%20Open-Source%20Plan.md).
Five design parameters each control one requirement:

| Part | File | Controls |
| --- | --- | --- |
| DP1 validator pin | `plugins/emhcl/skills/em-collaborate/scripts/install-emhcl.sh` | The emhcl release in Claude and in CI |
| DP2 vendored skill | `plugins/emhcl/skills/event-modeling-hcl/` | The language rules, copied without change from emhcl |
| DP3 Git port | `plugins/emhcl/skills/em-collaborate/references/git-operations.md` | Seven Git operations, bound to GitLab and GitHub tools |
| DP4 diagram publisher | `plugins/emhcl/skills/em-collaborate/references/diagrams.md` | Diagrams as Claude artifacts |
| DP5 CI templates | `ci-templates/emhcl.gitlab-ci.yml`, `.github/workflows/emhcl-model.yml` | The merge gate and the canonical diagram |

All procedures live in one skill, `em-collaborate`. Each command is a one-line
entry point to a procedure.

```
emhcl-plugin/
├── .claude-plugin/marketplace.json
├── plugins/emhcl/
│   ├── .claude-plugin/plugin.json
│   ├── skills/
│   │   ├── event-modeling-hcl/            # DP2: vendored upstream skill, unchanged
│   │   └── em-collaborate/
│   │       ├── SKILL.md
│   │       ├── references/                # procedures, git-operations, diagrams, configuration, compatibility
│   │       └── scripts/                   # install-emhcl.sh (DP1), check-compatibility.sh
│   ├── commands/                          # em-setup, em-view, em-validate, em-change, em-review, em-sync
│   └── evals/                             # claude plugin eval suite
├── ci-templates/emhcl.gitlab-ci.yml       # DP5 for GitLab
├── .github/workflows/emhcl-model.yml      # DP5 for GitHub Actions
├── scripts/sync-upstream-skill.sh         # copies the upstream skill and example at a tag
├── examples/pet-clinic/                   # upstream folder model, plus .emhcl.yml
└── tests/                                 # script and structure tests
```

## Diagrams

- GitLab Pages (or GitHub Pages) is the canonical view of the default branch.
- The team artifact mirrors the default branch inside Claude. em-sync
  republishes it to the same URL.
- em-change and em-review publish one proposal artifact for each MR.

Each title names the branch and the short commit SHA. A new artifact is
private; share it from the Share button of the artifact page.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Language changes go to
[emhcl](https://github.com/event-modeling-hcl/eventmodeling-hcl) and the
[specification](https://github.com/event-modeling-hcl/spec), not to this
plugin.
