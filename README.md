# Event Modeling HCL for Claude, Codex, and ChatGPT

Model business workflows and maintain
[Event Modeling HCL](https://github.com/event-modeling-hcl/spec) (`.em.hcl`)
files with shared method and language guidance. This repository provides two
Claude plugins, a local Codex skills distribution, and a portable plugin
for ChatGPT and Codex:

- `event-modeling-skills` holds 32 method skills and the `event-modeling-hcl`
  language skill. The method skills discover, review, and plan business models.
  The language skill owns HCL syntax and emhcl tool operations.
- `event-modeling-hcl-plugin` lets each person on a team view, change, and review the model
  through Claude. A change reaches the default branch only through a merge
  request in GitLab or GitHub, which a person reviews and merges. Claude Code
  installs `event-modeling-skills` as a dependency.

Both plugins use Apache-2.0 and release together as v0.2.0.
They target specification v0.8.0 and emhcl v0.17.0 or newer.
The method text uses original wording based on community ideas.
Event Modeling comes from Adam Dymitruk at Adaptech Group.
This project also credits [Martin Dilger](https://github.com/dilgerma).
See [the Event Modeling introduction](https://eventmodeling.org/posts/what-is-event-modeling/)
and [the packaged attribution](plugins/emhcl-skills/NOTICE).

| Surface | Modeling guidance | Repository collaboration | Diagrams |
| --- | --- | --- | --- |
| Claude plugins | 32 method skills and the HCL language skill | Six procedures through GitLab or GitHub MCP | Artifacts when supported; otherwise unchanged HTML |
| Local Codex CLI and IDE | The same 33 modeling skills | The same six procedures through configured Git MCP tools and a shell | Unchanged local HTML; no hosted team-artifact service |
| ChatGPT and Codex plugin | The same 33 modeling skills | The same six procedures when a shell and configured Git MCP tools are available | Unchanged local HTML; no hosted team-artifact service |

See [Codex skills setup](platforms/codex/README.md) and
[ChatGPT plugin setup](platforms/chatgpt/README.md).
The OpenAI plugin includes all 34 skills in one package.
Installation does not grant repository access or provide a shell.

## What it does

| Command | What it does | Writes to Git |
| --- | --- | --- |
| `em-setup` | Checks the connector, the validator, and `.emhcl.yml`. Proposes `.emhcl.yml` through an MR when it is missing. | Only an MR |
| `em-view` | Shows a branch as a diagram and answers questions about it | No |
| `em-validate` | Validates a branch with a profile and explains each diagnostic in plain words | No |
| `em-change` | Turns a request in plain words into edits, validates them, publishes a diagram, and opens an MR | A new branch and an MR |
| `em-review` | Validates the head of an MR, lists the changed slices, and publishes a diagram | One comment |
| `em-sync` | Republishes the shared team artifact from the default branch | No |

In Cowork and Claude Code, run a command as `/event-modeling-hcl-plugin:em-change`. In Claude chat,
ask in plain words; Claude uses the matching procedure. The plugin never merges
and never writes to the default branch.

## Install for Claude

In Claude Code, add the marketplace and install the collaboration plugin:

```sh
claude plugin marketplace add event-modeling-hcl/event-modeling-hcl-plugin
claude plugin install event-modeling-hcl-plugin@event-modeling-hcl
```

Claude Code also installs `event-modeling-skills`. To use only the skills,
without the Git procedures, install `event-modeling-skills@event-modeling-hcl`.

In chat and Cowork, install both plugins separately from Customize > Plugins.
Add this repository through Add > Add marketplace, or upload each plugin folder
as its own ZIP through Add > Upload plugin.
Each ZIP must contain `.claude-plugin/plugin.json` at its root or inside one top-level folder.
Do not upload a ZIP of the whole marketplace repository.

Skills load in chat, Cowork, and Claude Code.
Business modeling in plain words needs no shell or Git connector.
The collaboration procedures also need a shell, network access, and a Git connector.
The shell must run the pinned emhcl program and its installer.
If those tools are unavailable, the procedure stops rather than claiming a result.
Artifact publication depends on the app.
If publication is unavailable, the procedure returns the generated HTML file instead of a diagram link.
Installation alone does not prove that a procedure works.
See [the release test procedure](CONTRIBUTING.md#manual-tests-for-each-release) for the required app and Git host runs.

If you installed the former `emhcl` plugin, uninstall it with
`claude plugin uninstall emhcl@event-modeling-hcl`, then install
`event-modeling-hcl-plugin@event-modeling-hcl`. The marketplace name remains
`event-modeling-hcl`; the CLI remains `emhcl`.

If you installed the former `emhcl-skills` plugin, uninstall it with
`claude plugin uninstall emhcl-skills@event-modeling-hcl`, then install
`event-modeling-skills@event-modeling-hcl`. The source folder remains
`plugins/emhcl-skills/`. Both plugins use the repository tag `v0.2.0`.

## Install for local Codex

You need Python 3 to build and install the package. From this checkout, run:

```sh
python3 scripts/build-codex.py
python3 scripts/install-codex.py --source dist/codex --project /path/to/model-repo
```

Replace `/path/to/model-repo` with your model repository. The installer places
the 34 skills in its `.agents/skills/` directory. Use `--user` instead of
`--project` to install into `~/.agents/skills/` for all projects.
It refuses existing skill conflicts; managed upgrades require `--update`.
Restart Codex after installation.

Ask `$em-collaborate em-setup for OWNER/REPOSITORY`, or request `em-view`,
`em-validate`, `em-change`, `em-review`, or `em-sync` in plain words.
Configure the GitHub or GitLab MCP tools in Codex before collaboration.
The package does not install credentials or a connector. Without those tools,
you can still use the method and language skills for local modeling.

See [Codex setup and acceptance checks](platforms/codex/README.md) for
standalone installation, upgrades, and diagram-delivery limits.

## Install the ChatGPT and Codex plugin

From this checkout, build the plugin and register the repository marketplace:

```sh
python3 scripts/build-chatgpt.py
codex plugin marketplace add .
```

The builder writes a portable `plugin.json` and `skills/` under `dist/chatgpt`.
Use an absent or empty output directory. The builder never replaces an existing package.
The repository marketplace points to that default output.
Restart the ChatGPT desktop app, select Event Modeling HCL in the Plugins Directory,
and install `event-modeling-hcl-plugin`.
Start a new conversation and ask it to model your business workflow.

You can also install it in Codex:

```sh
codex plugin add event-modeling-hcl-plugin@event-modeling-hcl
```

In Codex, start a new session and invoke a plugin skill with its plugin prefix,
for example `$event-modeling-hcl-plugin:em-collaborate em-view for OWNER/REPOSITORY`.
Use either the plugin or the standalone Codex skills, not both in the same session.
The plugin bundles no Git server, credentials, or hosted artifact service.
Repository procedures require a shell, network access, and configured Git MCP tools.
Without those tools, the procedures stop. Business modeling still needs no repository.
See [the setup guide](platforms/chatgpt/README.md) for rebuilds and manual acceptance scenarios.
The package follows the [OpenAI plugin build guide](https://developers.openai.com/plugins/build/plugins).

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
  - remote: https://raw.githubusercontent.com/event-modeling-hcl/event-modeling-hcl-plugin/v0.2.0/ci-templates/emhcl.gitlab-ci.yml
    inputs:
      plugin_ref: v0.2.0
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
    uses: event-modeling-hcl/event-modeling-hcl-plugin/.github/workflows/emhcl-model.yml@v0.2.0
    with:
      plugin_ref: v0.2.0
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

[docs/design.md](docs/design.md) describes the design and the remaining risks.
Five design parameters each control one requirement:

| Part | File | Controls |
| --- | --- | --- |
| DP1 validator pin | `plugins/emhcl/skills/em-collaborate/scripts/install-emhcl.sh` | The emhcl release in Claude and in CI |
| DP2 language skill | `plugins/emhcl-skills/skills/event-modeling-hcl/`, `references/compatibility.md` | The language rules, from the plugin `event-modeling-skills`, and the emhcl range that they support |
| DP3 Git port | `plugins/emhcl/skills/em-collaborate/references/git-operations.md` | Seven Git operations, bound to GitLab and GitHub tools |
| DP4 diagram publisher | `plugins/emhcl/skills/em-collaborate/references/diagrams.md` | Diagrams as Claude artifacts |
| DP5 CI templates | `ci-templates/emhcl.gitlab-ci.yml`, `.github/workflows/emhcl-model.yml` | The merge gate and the canonical diagram |

All procedures live in one skill, `em-collaborate`. Each command is a one-line
entry point to a procedure. [docs/design.md](docs/design.md) describes the
design as built: the design matrix, the contract of each part, and the
residual risks.

```
event-modeling-hcl-plugin/
├── .claude-plugin/marketplace.json
├── .agents/plugins/marketplace.json       # OpenAI marketplace, selects dist/chatgpt
├── plugins/emhcl/
│   ├── .claude-plugin/plugin.json         # depends on event-modeling-skills
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
├── scripts/build-codex.py                 # standalone local Codex skills
├── scripts/install-codex.py               # guarded installation of those skills
├── scripts/build-chatgpt.py               # portable plugin for ChatGPT and Codex
├── platforms/                            # setup and manual acceptance scenarios
├── examples/pet-clinic/                   # upstream folder model, plus .emhcl.yml
└── tests/                                 # script and structure tests
```

## Diagrams

- GitLab Pages (or GitHub Pages) is the canonical view of the default branch.
- The team artifact mirrors the default branch inside Claude. em-sync
  republishes it to the same URL.
- em-change and em-review publish one proposal artifact for each MR.

Each title names the branch and the short commit SHA.
If the app can publish artifacts, a new artifact is private.
Use the Share button on its page to grant access.
If the app cannot publish artifacts, use the returned HTML file.
That file has no shared artifact URL.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Language changes go to
[emhcl](https://github.com/event-modeling-hcl/eventmodeling-hcl) and the
[specification](https://github.com/event-modeling-hcl/spec), not to this
plugin.
