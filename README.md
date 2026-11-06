# emhcl plugins for Claude

Two open-source Claude plugins for teams that keep an event model in
[Event Modeling HCL](https://github.com/event-modeling-hcl/spec) (`.em.hcl`)
files:

- `emhcl-skills` holds 32 method skills and the `event-modeling-hcl`
  language skill. The method skills discover, review, and plan business models.
  The language skill owns HCL syntax and emhcl tool operations.
- `emhcl` lets each person on a team view, change, and review the model
  through Claude. A change reaches the default branch only through a merge
  request in GitLab or GitHub, which a person reviews and merges. It installs
  `emhcl-skills` as a dependency.

The plugins target specification v0.8.0 and emhcl v0.17.0 or newer.
The existing `emhcl` plugin and the upstream language content use
Apache-2.0. Release of the restated method content awaits source-license review.
See [contract/CREDITS.md](contract/CREDITS.md). A passing text-overlap scan
does not establish license clearance.

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

Add the marketplace and install the plugins:

```sh
claude plugin marketplace add event-modeling-hcl/emhcl-plugin
claude plugin install emhcl@event-modeling-hcl
```

The second command also installs `emhcl-skills`. To use only the skills,
without the Git procedures, install `emhcl-skills@event-modeling-hcl`.

## The method skills

Each method writer owns one part of the model. Writers exchange requests,
questions, decisions, and evidence through the model. They do not call other
method writers by name. The orchestrator selects writers by responsibility.
The language skill is their shared authority for HCL syntax and tool operations.

The shared rules are in [contract/method.md](contract/method.md).
Section K13 holds the complete edit policy, including locked workflows and
shared consumers. [contract/hcl-binding.md](contract/hcl-binding.md) maps model
parts to HCL. `scripts/build-contract.sh` publishes these rules inside the
installed skills. Edit the canonical files, not the generated references.
See [the skill boundaries](docs/design.md#skill-boundaries-and-authorities).

To model a domain from start to end, ask for a complete event model. The skill
`eventmodeling-orchestrating-workflow` then runs the gates of the contract in
order. To do one step, ask for that step, for example "list the events of this
domain" or "write the scenarios of this command".

If a discussion follows screens instead of work, ask for a paper-world reset.
The event discovery and workshop skills walk one real case through its actors,
decisions, information, and handoffs. They keep source evidence and real system
actors. The reset does not add a gate or require a separate paper model.

Use Axiomatic Design when reviewing skill responsibilities or choosing software
boundaries after business discovery. It is not a required workshop step.

For a live group session, use `eventmodeling-facilitating-workshop`. It manages
participants and time, while the part writers record the model. For syntax-only
repairs, formatting, conversion, or language explanations, use
`event-modeling-hcl` without repeating business discovery. Business-only work
needs no HCL file or CLI run.

The broad `event-modeling` skill is retired. Use the orchestrator for a complete
model, the facilitator for a live session, or the specialist for one model part.
The shared contract preserves the retired skill's business and permission rules.

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
  - remote: https://raw.githubusercontent.com/event-modeling-hcl/emhcl-plugin/emhcl--v0.2.0/ci-templates/emhcl.gitlab-ci.yml
    inputs:
      plugin_ref: emhcl--v0.2.0
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
    uses: event-modeling-hcl/emhcl-plugin/.github/workflows/emhcl-model.yml@emhcl--v0.2.0
    with:
      plugin_ref: emhcl--v0.2.0
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
| DP2 language skill | `plugins/emhcl-skills/skills/event-modeling-hcl/`, `references/compatibility.md` | The language rules, from the plugin `emhcl-skills`, and the emhcl range that they support |
| DP3 Git port | `plugins/emhcl/skills/em-collaborate/references/git-operations.md` | Seven Git operations, bound to GitLab and GitHub tools |
| DP4 diagram publisher | `plugins/emhcl/skills/em-collaborate/references/diagrams.md` | Diagrams as Claude artifacts |
| DP5 CI templates | `ci-templates/emhcl.gitlab-ci.yml`, `.github/workflows/emhcl-model.yml` | The merge gate and the canonical diagram |

All procedures live in one skill, `em-collaborate`. Each command is a one-line
entry point to a procedure. [docs/design.md](docs/design.md) describes the
design as built: the design matrix, the contract of each part, and the
residual risks.

```
emhcl-plugin/
├── .claude-plugin/marketplace.json
├── plugins/emhcl/
│   ├── .claude-plugin/plugin.json         # depends on emhcl-skills
│   ├── skills/em-collaborate/
│   │   ├── SKILL.md
│   │   ├── references/                    # procedures, git-operations, diagrams, configuration, compatibility
│   │   └── scripts/                       # install-emhcl.sh (DP1), check-compatibility.sh
│   ├── commands/                          # em-setup, em-view, em-validate, em-change, em-review, em-sync
│   └── evals/                             # claude plugin eval suite
├── plugins/emhcl-skills/
│   ├── .claude-plugin/plugin.json
│   ├── skills/
│   │   ├── event-modeling-hcl/            # DP2: language, tools, generated permissions and binding
│   │   └── eventmodeling-*/               # 32 method skills with generated contract references
│   └── evals/                             # method, business-only, and HCL behavior cases
├── contract/                              # method contract and HCL binding (DP0)
├── ci-templates/emhcl.gitlab-ci.yml       # DP5 for GitLab
├── .github/workflows/emhcl-model.yml      # DP5 for GitHub Actions
├── scripts/build-contract.sh              # publishes installable shared authorities
├── scripts/sync-upstream.sh               # copies the example at a tag, writes compatibility.md
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
