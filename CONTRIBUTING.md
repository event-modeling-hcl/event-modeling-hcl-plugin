# Contributing

Thank you for helping. This repository holds two plugins: `event-modeling-hcl-plugin`, which adds
team procedures on top of emhcl, and `event-modeling-skills`, the home of the emhcl
agent skills. Put each change in the part that owns it:

| Change | Where |
| --- | --- |
| The Event Modeling HCL language, diagnostics, or the diagram page | Upstream: [eventmodeling-hcl](https://github.com/event-modeling-hcl/eventmodeling-hcl) or [spec](https://github.com/event-modeling-hcl/spec) |
| How agents write, repair, and validate `.em.hcl` | `plugins/emhcl-skills/skills/event-modeling-hcl/` |
| A rule that more than one method skill uses | `contract/method.md`, including K13 edit permissions, or `contract/hcl-binding.md` for its encoding. Then run `scripts/build-contract.sh`. |
| One step of the method | `plugins/emhcl-skills/skills/eventmodeling-<step>/` and its three evals in `plugins/emhcl-skills/evals/` |
| How Claude installs emhcl | `plugins/emhcl/skills/em-collaborate/scripts/install-emhcl.sh` |
| A Git connector tool name or parameter | `plugins/emhcl/skills/em-collaborate/references/git-operations.md` only |
| How diagrams become artifacts | `plugins/emhcl/skills/em-collaborate/references/diagrams.md` |
| A procedure | `plugins/emhcl/skills/em-collaborate/references/procedures/` |
| CI | `ci-templates/` and `.github/workflows/emhcl-model.yml` |
| Codex packaging, paths, or installation | `scripts/build-codex.py`, the Codex installer, and `platforms/codex/` |
| ChatGPT and Codex plugin packaging or marketplace discovery | `scripts/build-chatgpt.py`, `.agents/plugins/marketplace.json`, and `platforms/chatgpt/` |

Rules that keep the design uncoupled:

- Do not edit `compatibility.md`, a `references/contract.md`, or the generated
  language references `edit-policy.md` and `hcl-binding.md` by hand.
  Run `scripts/sync-upstream.sh <tag>` or `scripts/build-contract.sh`.
- A method skill never names another method writer. It writes only its own
  model part and sends other changes as request records. It uses the language
  skill as the shared authority for HCL syntax and tools.
- Put shared permissions in K13 of `contract/method.md`. The generator
  includes K13 in every method contract and in the language skill's policy.
- A change to the language skill `event-modeling-hcl` that follows a new
  emhcl release changes `metadata.spec_version` and `metadata.emhcl_min` in
  its front matter. Then run `scripts/sync-upstream.sh <tag>`.
- Do not put an emhcl version in a CI template. The tests fail when you do.
- Only `install-emhcl.sh` reads `emhcl_version`.
- A procedure uses only the seven Git operations. It never merges and never
  writes to the default branch.
- A command stays a one-line entry point to a procedure.
- Keep method and language changes in the shared sources, not platform
  adapters. Build platform outputs into `dist/`; do not commit generated
  copies or treat an installed package as the source of truth.
- Preserve `LICENSE` and the methodology attribution in
  `plugins/emhcl-skills/NOTICE` in generated distributions.

## Tests

```sh
python3 -m unittest discover -s tests -p 'test_*_package.py' -v
python3 scripts/build-codex.py
python3 scripts/build-chatgpt.py
sh tests/install-emhcl.test.sh     # installer, against a fake release, no network
sh tests/structure.sh              # structure, contract copies, skill names, example, claude plugin validate
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
claude plugin eval . --trust-plugin --tag business
claude plugin eval . --trust-plugin --tag language --allow-tools Write Edit Bash
claude plugin eval . --trust-plugin --tag write --allow-tools Write
```

The business cases cover plain-language modeling without file or CLI work.
The language cases include the migrated HCL cases and permission boundaries.
Grant writing tools only for cases that create or change sandbox fixtures.

The evals cannot load a Git connector, because a plugin eval loads only MCP
servers that the plugin declares, and `emhcl` declares none. So the evals
cover language tasks, method skills, and safety rules. The manual test below
covers the Git procedures. An eval of a plugin path loads only that plugin, so
the evals of `event-modeling-hcl` and the method skills live in
`event-modeling-skills`.

Platform packaging tests run without a model account. They exercise generated
files and installation safety, not response quality. For Codex and ChatGPT
runtime checks, use the acceptance scenarios in `platforms/codex/` and
`platforms/chatgpt/`. Run connector-backed scenarios only in a test repository.
Building a package does not authorize a remote write.

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

Both plugins share the repository release `v0.2.0`. The release tag is not an emhcl binary version.
Future repository releases use `v<version>` and release both plugins together.

1. Run the automated tests above and record their commands and results.
2. Complete the manual tests below and record each result separately.
3. Set both plugin manifest versions to `0.2.0` and update the release entries in `CHANGELOG.md`.
4. Use `v0.2.0` in the CI include examples and as `plugin_ref`.
5. Prepare one archive per plugin and complete directory validation as described below.
6. After reviewing the release files and results, manually create the single repository tag `v0.2.0`.

Do not create per-plugin tags. The maintainer creates the repository tag manually.
These instructions do not create, commit, tag, or push a release.

### Plugin archives and directory validation

Follow the [plugin build guide](https://claude.com/docs/plugins/build)
and the [submission checklist](https://claude.com/docs/plugins/pre-submission-checklist).
Package `plugins/emhcl` and `plugins/emhcl-skills` in separate ZIP archives.
Each archive must contain `.claude-plugin/plugin.json` at its root or inside one top-level plugin folder.
Do not upload an archive of the whole repository as one plugin.

Run `claude plugin validate plugins/emhcl` and `claude plugin validate plugins/emhcl-skills`.
These commands test file syntax and schemas, not all directory requirements or behavior.
For each plugin folder, open the [developer portal](https://claude.ai/directory/manage).
Select `Submit new`, then `Plugin bundle`, and enter the repository on the `Source` step.
Select the individual plugin folder and select `Validate`.
Record the commit, folder, result, blocking findings, warnings, and reviewer holds.
Fix blocking findings before submission.
After publishing fixes to the repository, select `Re-validate` on the same `Source` step.
Submit each plugin separately, not the marketplace repository as one plugin.

Make sure that each plugin contains a README with at least 40 words outside code blocks.
It must describe usage and the data that the plugin sends, fetches, or runs.
Each plugin also needs a license file or a manifest license field.
All runtime files must remain inside the installed plugin folder.
A successful portal report does not establish successful manual behavior tests or directory approval.

### OpenAI plugin package

The OpenAI plugin uses the portable format in the
[OpenAI plugin build guide](https://developers.openai.com/plugins/build/plugins).
Build `dist/chatgpt` with `python3 scripts/build-chatgpt.py`.
Keep its root `plugin.json`, `skills/`, `LICENSE`, and `NOTICE` together.
The repository marketplace at `.agents/plugins/marketplace.json` points to that output.

Use [the ChatGPT setup guide](platforms/chatgpt/README.md) for local installation and manual tests.
Do not install the standalone Codex skills alongside the plugin in the same session.
They contain the same skills.
Record local installation, ChatGPT discovery, and authenticated procedure results separately.
Do not report a desktop test as a successful ChatGPT web test.

Public directory submission is separate from local installation.
Follow the [OpenAI submission guide](https://developers.openai.com/plugins/deploy/submission)
after the manual checks pass.
The maintainer must supply the verified publishing identity and complete the portal review.
Do not publish credentials or claim directory approval from a successful local build.


## Manual tests for each release

These are required manual tests, not recorded successes.
Automated structure tests and model evals do not establish chat, Cowork, or Git connector behavior.
Record `Pass`, `Fail`, or `Not run` for every app, host, and step.
Include the date, tester, app version, plugin versions, commit, connector, evidence links, and any failure reason.
Do not report a surface as tested when its result is `Not run`.

Test Claude chat on claude.ai, Cowork, and Claude Code separately.
For each app, repeat the collaboration steps with GitLab and GitHub.
Use a disposable project with the pet-clinic example, `.emhcl.yml`, the CI template at `v0.2.0`, and fast-forward merges.
Before the tag exists, record the candidate commit used for CI.
After the maintainer creates the tag, make sure that `v0.2.0` resolves to that commit.

In Claude Code, load both folders with
`claude --plugin-dir ./plugins/emhcl --plugin-dir ./plugins/emhcl-skills`.
Also test installation from the repository marketplace to exercise automatic dependency installation.
Only Claude Code supports automatic plugin dependencies.
In claude.ai, open `Customize > Plugins > Add > Upload plugin` and upload each plugin archive separately.
Install both plugins separately in Cowork too.
Open a chat or Cowork task and ask Claude which plugin skills it can use.
Make sure that both plugins load, including the language and method skills.
Commands load as skills in chat. Test their behavior with plain-language requests there.

Collaboration requires shell execution, permission to download and run emhcl, network access, and a connected Git connector.
Connect the GitLab or GitHub connector separately. These plugins do not bundle a connector.
Record missing prerequisites as a blocked test, not a successful collaboration test.
Where artifact publishing is unavailable, accept the generated HTML file and the stated reason instead of an artifact URL.
For `em-sync`, record URL reuse as `Not run` on those surfaces and test the HTML fallback.

| Step | Pass when |
| --- | --- |
| em-setup on a project without `.emhcl.yml` | It reports each check and opens one MR that adds `.emhcl.yml`. |
| em-view on the default branch | The artifact or fallback HTML title is `<project> <branch> @ <short SHA>`. The SHA is the branch head. |
| em-validate with `strict` | The lines equal a local `emhcl validate --profile strict` at that commit. |
| em-change "add a slice where the owner cancels an appointment" | A new branch starts from the snapshot commit. One commit and an MR contain the change. The MR includes the artifact link or explains its absence. It is a Draft when `strict` fails. |
| em-change that cannot pass core validation | Nothing reaches Git, and the report names the diagnostics. |
| em-review on the appointment-cancellation MR | One comment reports validation and changed slices. It includes a diagram link or explains the HTML fallback. |
| em-sync twice | Where publishing is supported, the second run republishes to the same URL. Otherwise, both runs return the HTML fallback and explain why no artifact exists. |
| A request to merge the MR | Claude declines. |
| CI after the merge | Pages shows the new commit in its title. |

Test representative method and language requests in each app as well.
Compare their output with a session without the plugins.
Record whether Claude selects the responsible skill, preserves supplied business rules, and reports unknown decisions.
For HCL requests, record the emhcl validation result separately from the model response.
Do not treat skill discovery, archive upload, or portal validation as proof of correct modeling behavior.
