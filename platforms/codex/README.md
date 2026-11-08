# Event Modeling skills for Codex CLI and IDE

Use this package to install all 33 method/language skills and the
`em-collaborate` skill into Codex's local skill discovery tree. It runs in
Codex CLI or IDE, not through a hosted backend. The method rules, HCL
language references, collaboration procedures, validator installer, and
compatibility checker come from the same canonical sources as the Claude
plugin. Building or installing this package does not change that plugin.

## Before you begin

You need Python 3 with its standard library to build or install. To run
collaboration procedures, Codex also needs shell access and a configured,
authenticated GitHub MCP server or GitLab MCP server (GitLab 19.4 or later).
Check your Codex MCP configuration and tool schemas before invoking
`em-setup`. A local Git checkout, Git transport, and `gh` are not required.
The unchanged validator installer needs `curl` or `wget`, an SHA-256 tool,
and archive extraction tools; if downloading fails, it can use Go. Each
model repository pins its validator release in `.emhcl.yml`.

The package preserves the repository `LICENSE` and the method plugin's
`NOTICE` under `skills/.emhcl-codex/`. The notice credits the methodology
and upstream language content. The original method wording uses Apache-2.0.
The credits do not claim that third-party methodology articles use that license.

## Build from the repository

From the repository root, build the default `dist/codex` package:

```sh
python3 scripts/build-codex.py
```

To choose a different package directory, use `--output`:

```sh
python3 scripts/build-codex.py --output "$HOME/event modeling codex"
```

The output contains `skills/`, `install-codex.py`, this README, and a
SHA-256 file-inventory manifest. Copy the whole output directory to another
machine if needed; it has no runtime dependency on the source checkout.
Builds reject missing sources or unresolved local Markdown references.

## Install into a project

Choose exactly one installation scope. For project-local discovery, run:

```sh
python3 dist/codex/install-codex.py --project "/path/to/model project"
```

Replace `/path/to/model project` with your project directory. This creates
`.agents/skills` inside that directory. Start Codex in that project and
confirm that `$em-collaborate` and `$event-modeling-hcl` appear as skills.
Restart an existing Codex session if it has not discovered the installation.

For user-wide discovery, run:

```sh
python3 dist/codex/install-codex.py --user
```

This installs into `~/.agents/skills`. For an explicit skills directory, run:

```sh
python3 dist/codex/install-codex.py --destination "$HOME/staging/.agents/skills"
```

An arbitrary destination is useful for staging and tests, but Codex only
discovers it if it is in a supported project or user skill location. The
installer never chooses a user's skills directory implicitly. From a source
checkout, you can also use `scripts/install-codex.py --source PACKAGE` with
the same scope flags. Replace `PACKAGE` with a complete built package path.
The bundled installer finds its adjacent package automatically.

## Invoke a workflow

In a Codex CLI or IDE conversation, select the skill and name the procedure:

```text
$em-collaborate em-setup for acme/orders
$em-collaborate em-view for acme/orders
$em-collaborate em-validate for acme/orders
$em-collaborate em-change for acme/orders: add the supplied cancellation rule
$em-collaborate em-review for https://github.com/acme/orders/pull/42
$em-collaborate em-sync for acme/orders
```

These are skill invocations and plain procedure names, not Claude plugin
slash commands. Local `.em.hcl` work without a repository uses
`$event-modeling-hcl`. Business-only modeling can use the method skills
without a shell, validator, or MCP server.

The collaboration skill locates its unchanged scripts from the actual
installed `em-collaborate/SKILL.md` path, not a working-directory assumption
or `${CLAUDE_SKILL_DIR}`. It quotes script paths so installations with spaces
work. Keep the entire skill tree together: language references use sibling
skill links, and the compatibility checker reads its own relative
`../references/compatibility.md`.

Codex CLI 0.162.1 shortens a `SKILL.md` file that is larger than about
8,000 bytes when a person invokes the skill by name. The builder keeps each
`SKILL.md` at 8,000 bytes or less. If a skill is longer, the builder moves its
last complete sections, unchanged, to `instructions-continued.md` in the same
skill folder. `SKILL.md` links to that file and lists the moved sections.

All collaboration procedures keep the seven-operation Git port and its
existing safety rules. They never merge, approve, close an MR, or write to
the default branch. The host's exposed MCP operations must satisfy the
canonical bindings. If a required operation is absent, the skill stops and
names it rather than substituting a local Git backend.

## Understand diagram limitations

Codex renders the unchanged `emhcl diagram` HTML to a local file. It does not
provide the Claude hosted-artifact publisher, hosted comments, or artifact
sharing controls. Reports identify the local HTML path and `Artifact: none`.
MR descriptions and comments use the no-diagram-link alternative; local
paths and invented links are never presented as team-accessible URLs.

`em-sync` still snapshots and validates the default branch and renders its
HTML. It explicitly reports that the shared team artifact was **not**
updated. It leaves `team_artifact_url` and `.emhcl.yml` unchanged, even when
the URL is empty. Share the file through an approved channel yourself if
needed. `canonical_url`, when configured, remains the CI-maintained
canonical view, not a page hosted by Codex.

## Rebuild and update safely

Rebuilding the same package directory is repeatable. The builder only
replaces or removes files it previously generated and whose hashes still
match its manifest. It preserves unrelated files and rejects collisions,
modified managed files, source-tree output targets, and symlink paths.
There is no force-overwrite flag. If you edited generated files, preserve
your work separately and build into a fresh directory instead.

To update an installation, rebuild the package and explicitly request an
update using the same scope:

```sh
python3 scripts/build-codex.py
python3 dist/codex/install-codex.py --project "/path/to/model project" --update
```

The installer verifies the package inventory before creating a destination.
It checks every conflict before writing, refuses existing unowned skill
directories even if individual filenames do not collide, and refuses
updates when managed files were edited or removed. It preserves unrelated
skills and files, and removes only obsolete unchanged files recorded in
its own installation manifest. Keep that manifest with the installation.
Do not run concurrent builders or installers against the same destination.
On systems where `/tmp` is a symlink (including macOS), use a physical
directory path instead; symlinked parents are intentionally rejected.
Filesystem failures during replacement can leave a partial update; use a
fresh destination if the managed manifest no longer matches after a failure.

For maintainer verification, run the Python regression suite from the
source repository:

```sh
python3 -m unittest discover -s tests -p 'test_codex_package.py'
```

## Check the runtime before release

Packaging tests do not verify connector authentication or model behavior.
Use a disposable model repository with the pet-clinic example and repeat
these scenarios for each supported Git host. Record the Codex version,
available MCP operations, commit IDs, validator output, and observed result.

| Scenario | Accept when |
| --- | --- |
| Discovery and missing connector | Codex loads the project-installed skill, reads em-setup, and stops at S1 with the missing Git MCP prerequisite rather than inventing tools |
| em-setup | Reports connector, configuration, pinned validator, and compatibility results; proposes a missing configuration only through a new branch and MR |
| em-view and em-validate | Reads a complete commit-addressed snapshot; diagnostics match the pinned binary; diagram output is unchanged local HTML |
| em-change | Validates the exact proposed files before committing only to a new branch from the snapshot; merge-profile errors make the MR Draft; core errors prevent Git writes |
| em-review | Reads the MR base/head, reports validation and changed slices, and posts only the requested comment without approval or merge |
| em-sync | Uses only the default branch, delivers local HTML, leaves configuration unchanged, and explicitly reports that no hosted artifact was updated |
| Forbidden merge | Refuses to merge, approve, close the MR, or write to the default branch |
| Installation with spaces | Finds installed scripts by their loaded skill path and runs the compatibility check and pinned validator with quoted paths |

An unavailable connector blocks remote checks, not local method/language
work. A local build or successful validator run is not evidence that the
remote collaboration scenarios passed.
