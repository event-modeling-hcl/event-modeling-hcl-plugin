# Changelog

This file records releases of both plugins in this repository.
Both plugins use version 0.1.0 for the first combined release.
The maintainer creates the repository tag `v0.1.0` manually.

## [Unreleased]

### Added

- A portable ChatGPT and Codex plugin with all 34 skills, built with `python3 scripts/build-chatgpt.py`.
- A repository marketplace for local plugin installation and a guide for desktop acceptance tests.
- A standalone Codex skills package with a guarded project or user installer.
- Package tests for detached resources, source references, deterministic builds, and destination safety.
- A platform design with traced requirements, influence analysis, module contracts, and explicit runtime limits.
- Plugins Directory listing text in `extensions.com.openai.interface` of the plugin manifest: name, descriptions, category, and three starter prompts.
- A statement in each plugin skill that explicit user scope takes priority over optional skill guidance. Fixed permission, validation, and merge rules still apply.

### Fixed

- Both package builders use the current methodology `NOTICE` instead of the removed `contract/CREDITS.md`.
- The Codex adapter matches the current collaboration skill and preserves its validation and permission rules.
- Codex CLI 0.162.1 shortened an explicitly invoked `SKILL.md` above about 8,000 bytes. Three plugin skills and two standalone Codex skills lost their last sections. In the plugin skill `em-collaborate`, the lost text included the validation steps, the report rules, and the execution boundary. Both builders now keep each `SKILL.md` at 8,000 bytes or less. They move the last complete sections to a linked `instructions-continued.md`.
- The plugin guide and the runtime preflight named `$em-collaborate` for Codex. Codex selects a plugin skill only with its plugin prefix, so they now name `$event-modeling-hcl-plugin:em-collaborate`.
- Resolved merge conflicts without restoring obsolete release tags or the old license-review caveat.

### Removed

- The unfinished Custom GPT upload bundle. Use the portable plugin instead of uploading knowledge files.

## [0.1.0]

This release includes `event-modeling-hcl-plugin` and `event-modeling-skills`.
Both plugins use Apache-2.0.
The repository tag selects both plugins and the shared CI templates.

### Added

The release includes these components:

- The `event-modeling-hcl` marketplace with both plugins.
- The `em-collaborate` skill with six team procedures and their commands: `em-setup`, `em-view`, `em-validate`, `em-change`, `em-review`, and `em-sync`.
- The `event-modeling-hcl` language skill 3.1.0 from emhcl v0.17.0, for specification v0.8.0.
- The 32 method skills for discovery, model parts, review, feedback, and delivery planning.
- The workflow orchestrator for complete models and the facilitator for live workshops.
- The shared method contract, including the K13 edit policy, and its HCL binding.
- The generated skill references that preserve workflow locks, shared-consumer permissions, and approval scope.
- The installer for the pinned emhcl release, with a SHA-256 comparison and a Go installation fallback.
- The compatibility script for the installed emhcl version and the language skill.
- The seven Git operations with bindings for GitLab and GitHub connectors.
- The diagram procedures for branch proposals and the default branch, with an HTML file fallback when artifact publication is unavailable.
- The GitLab CI template and reusable GitHub workflow for validation and Pages publication.
- The pet-clinic example with emhcl 0.17.0 pinned in `.emhcl.yml`.
- The scripts that generate contract references and compare the example with the upstream release.
- The installer tests, structure checks, and model-based evaluation cases.
- A README and the Apache-2.0 license text inside each plugin folder.
- The methodology attribution in the skills plugin's `NOTICE` file.

### Changed

If you used the earlier development names, update your installation:

- Replace `emhcl@event-modeling-hcl` with `event-modeling-hcl-plugin@event-modeling-hcl`.
- Replace `emhcl-skills@event-modeling-hcl` with `event-modeling-skills@event-modeling-hcl`.
- Use `/event-modeling-hcl-plugin:` as the command namespace in Cowork and Claude Code.

See [the installation instructions](README.md#install-for-claude) for the uninstall commands.
The marketplace remains `event-modeling-hcl`, and the command-line program remains `emhcl`.
Claude Code installs the skills plugin as a dependency of the collaboration plugin.
In chat and Cowork, install both plugins separately.

### Removed

The broad `event-modeling` skill is not part of this release.
Use the orchestrator for complete models, the facilitator for workshops, or the specialist for one model part.
Its shared permission rules remain in the method contract.
