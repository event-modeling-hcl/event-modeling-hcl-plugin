# Changelog

This file records the releases of the emhcl plugin for Claude. A release tag
has the form `emhcl--v<version>`, as `claude plugin tag` makes it.

## [Unreleased]

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
