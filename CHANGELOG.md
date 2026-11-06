# Changelog

This file records the releases of the emhcl plugin for Claude. A release tag
has the form `emhcl--v<version>`, as `claude plugin tag` makes it.

## [Unreleased]

### Changed

- Paper-world discovery now includes questions about information, decisions,
  handoffs, corrections, and delays in the event and workshop skills.
- Shared discovery rules retain source evidence, actual system actors, and
  command authority without restarting completed work or adding a paper model.
- The general Event Modeling skill makes the paper-to-software handoff explicit.

## [0.2.0]

### Added

- The plugin `emhcl-skills` 0.1.0, the home of the emhcl agent skills. It
  holds the skills `event-modeling` 1.0.0 and `event-modeling-hcl` 3.1.0, moved
  unchanged from emhcl v0.17.0 (specification v0.8.0), and 32 method skills
  that write one part of the model each and name no other skill.
- The method contract `contract/method.md` (K0 to K12), its HCL v0.8.0
  binding `contract/hcl-binding.md` (H0 to H11), and `contract/CREDITS.md`.
- `scripts/build-contract.sh`, which copies the contract sections that each
  method skill lists into its `references/contract.md`, and checks them with
  `--check`.
- `scripts/check-source-overlap.sh`, which reports text that the method content
  shares with the source skills of unknown license.
- Three eval cases for each method skill. The eval `author-slice` moved to
  `emhcl-skills`.

### Changed

- The plugin `emhcl` no longer vendors `event-modeling-hcl`. It depends on
  `emhcl-skills`, which Claude Code installs with it.
- The plugins support emhcl v0.17.0 and newer (specification v0.8.0), and
  were tested with v0.17.0. The example pins emhcl 0.17.0.
- `scripts/sync-upstream-skill.sh` became `scripts/sync-upstream.sh`. It copies
  the example model at an emhcl tag and writes `compatibility.md` from the
  front matter of `event-modeling-hcl`.

## [0.1.0]

### Added

- The plugin `emhcl` and the marketplace `event-modeling-hcl`.
- The skill `em-collaborate` with the procedures em-setup, em-view,
  em-validate, em-change, em-review, and em-sync, and one command for each.
- The vendored skill `event-modeling-hcl` 2.5.0 from emhcl v0.16.0
  (specification v0.7.0). The plugin supports emhcl v0.16.0 and newer, and
  was tested with v0.16.0.
- `install-emhcl.sh`, which installs the emhcl release that `.emhcl.yml` pins,
  with a SHA-256 check and a `go install` fallback. Claude and CI both run it.
- `check-compatibility.sh`, which compares an installed emhcl with the range of
  the vendored skill.
- The Git port: seven Git operations with bindings for the GitLab MCP server
  and the GitHub MCP server.
- The GitLab CI template `ci-templates/emhcl.gitlab-ci.yml` and the reusable
  GitHub workflow `.github/workflows/emhcl-model.yml`, with the jobs
  `emhcl-validate` and `pages`.
- `scripts/sync-upstream-skill.sh`, which copies the upstream skill and the
  pet-clinic folder model at an emhcl tag, and checks them with `--check`.
- The example model repository `examples/pet-clinic`.
- Script tests, structure tests, and a `claude plugin eval` suite.
