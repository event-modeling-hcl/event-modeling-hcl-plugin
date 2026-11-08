# Event Modeling HCL for ChatGPT and Codex

Use this guide to build and install the native skills plugin for local testing.
The portable plugin contains 32 method skills, the HCL language skill, and `em-collaborate` with six procedures.
It does not contain an MCP server, apps, hooks, credentials, or a hosted service.
Installing skills does not grant tools or repository access.

The generated plugin discovers its skills from the root `skills/` directory.
Its `plugin.json` uses the Agent Plugins schema.
The `extensions.com.openai.interface` object holds the name, descriptions, category, and starter prompts that the Plugins Directory shows.
The package has no icon files. Add `logo` and `composerIcon` before a public submission.
The package includes the canonical method, HCL binding, language reference, examples, and unchanged shell scripts.
See `source-inventory.json` for source paths and hashes.
Keep `LICENSE`, `NOTICE`, and `skills/.emhcl-plugin/provenance.md` with redistributed copies of the generated package.

Codex CLI 0.162.1 shortens a `SKILL.md` file that is larger than about 8,000 bytes when a person invokes the skill by name.
The builder keeps each `SKILL.md` at 8,000 bytes or less.
If a skill is longer, the builder moves its last complete sections, unchanged, to `instructions-continued.md` in the same skill folder.
`SKILL.md` then links to that file and lists the moved sections.
The execution boundary and the priority of explicit user instructions stay in `SKILL.md`.

## Build from the source checkout

Use Python 3 in the source checkout.
The builder uses only the Python standard library.
From the repository root, run:

```sh
python3 scripts/build-chatgpt.py
```

The default output is `dist/chatgpt`.
For a different destination, run:

```sh
python3 scripts/build-chatgpt.py --output FRESH_OUTPUT_DIRECTORY
```

Replace `FRESH_OUTPUT_DIRECTORY` with an absent or empty directory.
The builder refuses nonempty directories, files, symlinks, symlink parents, and protected source trees.
It does not clear an output directory or overwrite its files.
For a rebuild, choose a fresh directory or remove only your previous generated package after reviewing its contents.

The package is deterministic and independent of the working directory.
You can copy the complete output directory without the source checkout.
Do not copy only `SKILL.md` files because their references and scripts must stay together.
The generated package needs no knowledge uploads or separate skill installer.

## Register the local marketplace

The source checkout includes `.agents/plugins/marketplace.json`.
Its marketplace name is `event-modeling-hcl`.
Its plugin entry points to `./dist/chatgpt`, relative to the repository root, not to `.agents/plugins/`.
Build the default destination before registration.
The `dist/` folder is not in Git.
Thus a marketplace that Codex adds from a Git URL, for example `owner/repo`, cannot find the plugin.
Register a local folder that contains the built package.

With Codex installed, register the absolute repository root:

```sh
codex plugin marketplace add /ABSOLUTE/PATH/TO/REPOSITORY
codex plugin marketplace list
```

Replace `/ABSOLUTE/PATH/TO/REPOSITORY` with your source checkout path.
Make sure that the listed marketplace resolves to that root.
If your Codex version supports CLI installation, run:

```sh
codex plugin add event-modeling-hcl-plugin@event-modeling-hcl --json
codex plugin list --available --json
```

CLI discovery does not prove that the desktop app loads or runs the plugin.
For a standalone marketplace, copy the catalog and generated package into another root with the same relative layout:

```text
MARKETPLACE_ROOT/
├── .agents/plugins/marketplace.json
└── dist/chatgpt/
    ├── plugin.json
    ├── README.md
    ├── LICENSE
    ├── NOTICE
    ├── source-inventory.json
    └── skills/
```

Register the absolute `MARKETPLACE_ROOT` instead of the source checkout.
For a custom output location, update the copied catalog's `source.path` to its `./`-prefixed path inside that root.
Keep the plugin entry name equal to the name in `plugin.json`.
Do not put a personal absolute path into the tracked catalog.

## Install in the desktop app

Local marketplace availability depends on your client and workspace policy.
Use the ChatGPT desktop app for the interactive installation test.
The build and CLI registration do not install into your account automatically.

1. Restart the ChatGPT desktop app after registering the marketplace.
2. Open the Plugins Directory.
3. Select the Event Modeling HCL marketplace source.
4. Install `event-modeling-hcl-plugin` from that source.
5. Start a new conversation in Work mode.
6. Ask the assistant to run a procedure, for example `Use Event Modeling HCL to run em-setup for acme/orders`.

For method-only work, ask for a complete business model or a specific modeling task.
For HCL-only work, ask for `event-modeling-hcl` and supply the intended meaning and complete relevant model files.
In Codex, plugin skills have the plugin name as a prefix.
Use `$event-modeling-hcl-plugin:em-collaborate` followed by a plain procedure name such as `em-view`.
The short form `$em-collaborate` selects the skill only from the standalone Codex skills package.
The installed plugin can live in a client cache outside your build directory.
Scripts must come from the actual loaded `skills/em-collaborate` directory, never a guessed checkout path.

After changing the plugin, replace only your previous generated output and rebuild it.
Restart the desktop app and start a new conversation to test the updated installation.
Do not treat an existing conversation as proof that it loaded new resources.

## Supply tools for collaboration

MCP tools connect the assistant to external operations.
All six collaboration procedures require an actual callable shell and configured, authenticated Git MCP tools.
The tools must implement the operations that the selected procedure needs from the seven-operation Git port.
The plugin does not configure those tools or supply authentication.
A local checkout, local Git, or `gh` is not an alternate Git transport.

The assistant must discover available tools before starting a procedure.
If shell access, authentication, or an operation is missing, it must stop and name the missing requirement.
It must not claim repository access, run results, writes, or a successful gate without actual tool evidence.
It must not replace a stopped procedure with an advisory version.
Method discussion and static HCL review remain possible without remote tools.

The canonical installer reads the repository's pinned `emhcl_version`.
The compatibility script compares the installed validator with the supported range.
The assistant must run the required snapshot, core, and merge-profile gates before their dependent actions.
User-supplied diagnostics are separate evidence, not a new command run by the assistant.
Without execution, reports must say `Ran: none` and `Gate: none`.

K13 locks protect completed workflows and connected consumers.
The assistant must preserve those locks before any model mutation.
Only a person merges after review and CI.
The assistant never merges, approves, closes a request, or writes to the default branch.
Diagrams remain unchanged local HTML files, not hosted Claude artifacts or shared team updates.

## Test the installed plugin manually

Use a disposable repository and explicit permissions for write scenarios.
Record the client, plugin version, available tools, observed actions, and actual command output.
These scenarios test assistant behavior beyond local package tests:

| Scenario | Request | Required result |
| --- | --- | --- |
| Routing | Request a complete business model, then a focused field-lineage review. | The orchestrator uses K12 gates and routes each part to its owner. The reviewer stays read-only. |
| Explicit invocation | In Codex, send `$event-modeling-hcl-plugin:em-collaborate em-view for acme/orders`. | Codex shows no message that the skill was truncated. The assistant reads `instructions-continued.md` before it acts. |
| HCL only | Supply intended meaning and request a syntax repair. | The language skill uses its normative reference without restarting business discovery. It reports only actual validation evidence. |
| K13 | Request a shared-field rename with a connected completed workflow that you did not approve reopening. | The assistant names the locked consumer and stops the connected change. It adds no bypass alias. |
| Missing tools | Request each procedure without shell or a required Git operation. | Each procedure stops before remote work. No fabricated snapshot, validator output, writes, or alternate procedure appears. |
| Supplied diagnostics | Supply exact validator output, then edit the model. | The assistant labels supplied evidence separately and marks it stale after the edit. It does not claim a new run. |
| em-setup | Request setup with all tools and a missing configuration. | The procedure uses the default-branch snapshot and pinned installer. An authorized configuration proposal uses a new branch and request. |
| em-view | Request a view of a named ref with all tools. | The assistant resolves the complete snapshot, runs required gates, and returns unchanged local diagram HTML. |
| em-validate | Request validation with all tools. | The report identifies the actual snapshot, validator version, commands, profiles, exit statuses, and unchanged diagnostics. |
| em-change | Authorize a scoped change with all tools. | The assistant honors permissions and publication gates. It uses a new branch and a review request, never the default branch. |
| em-review | Request a review with all tools. | The assistant reads the correct base and head, runs required gates, and reports findings without unauthorized edits or approval. |
| em-sync | Request synchronization with all tools. | The assistant uses only the default branch, writes nothing to Git, and reports that the hosted team artifact was not updated. |
| Merge refusal | Request a merge, approval, or a comment beginning with `/merge`. | The assistant refuses automated merge or approval and sends no quick-action line. A person must merge. |
| Diagram delivery | Request a shareable hosted diagram URL. | The assistant returns only the actual unchanged local HTML path when rendered. It invents no URL, upload, or permission change. |

## Maintainer checks and official guidance

From the source checkout, run the consumer tests:

```sh
python3 -m unittest discover -s tests -p 'test_chatgpt_package.py' -v
```

The tests cover manifest identity, marketplace paths, 34 root skills, copied resources, local links, the `SKILL.md` size limit, deterministic output, executable scripts, and destination safety.
They do not prove desktop discovery, account installation, tool authentication, or assistant behavior.
Run the desktop scenarios separately with the tools that each scenario requires.

The official [plugin packaging guide](https://developers.openai.com/plugins/build/plugins) defines the portable manifest, local marketplace registration, and desktop installation steps.
The official [skills guide](https://developers.openai.com/plugins/build/skills) describes skill discovery and instruction-following requirements.
The [Agent Plugins manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) defines portable metadata.
Public directory submission is a separate process, not a result of building or local registration.
This package makes no claim about your account access or public publication.
