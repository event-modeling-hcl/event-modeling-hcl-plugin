---
name: em-collaborate
description: >-
  Team procedures for an Event Modeling HCL model (`.em.hcl` files) that lives
  in a GitLab or GitHub repository. Show a branch of the model as a diagram,
  validate it, turn a change request in plain words into a new branch and a
  merge request, review a model merge request or pull request, and mirror the
  default branch into a shared team artifact. Use this skill whenever a person
  asks to see, check, change, review, or merge the team's event model, its
  slices, or a merge request that changes the model, or runs em-setup,
  em-view, em-validate, em-change, em-review, or em-sync. The skill states the
  team rules: the plugin never merges and never writes to the default branch.
compatibility: >-
  Needs the GitLab MCP server (GitLab 19.4 or later) or the GitHub MCP server,
  a shell with curl or go, and the emhcl release that the model repository
  pins in .emhcl.yml. Needs the event-modeling-hcl skill of the plugin
  emhcl-skills, which the plugin emhcl installs as a dependency.
metadata:
  version: "0.2.0"
allowed-tools:
  - Bash(sh ${CLAUDE_SKILL_DIR}/scripts/install-emhcl.sh *)
  - Bash(sh ${CLAUDE_SKILL_DIR}/scripts/check-compatibility.sh *)
---

# em-collaborate

This skill holds the procedures that let a team view, change, and review one
event model through Claude. The model lives in a Git repository. A change
reaches the default branch only through a merge request (MR) that a person
reviews and merges in GitLab or GitHub.

The language itself belongs to the skill `event-modeling-hcl` of the plugin
`emhcl-skills`. The plugin `event-modeling-hcl-plugin` installs `emhcl-skills` as a dependency.
Load `event-modeling-hcl` before you write, repair, or explain `.em.hcl` text.
This skill adds only the team procedures.

## Rules that always apply

1. Never write to the default branch. Never merge, approve, or close an MR.
   Never call `accept_merge_request`, `merge_pull_request`, or another tool
   that merges.
2. Use only the seven Git operations in
   [references/git-operations.md](references/git-operations.md). Write to Git
   only with commit-branch on a new branch that this procedure made, then
   open-mr or comment-mr.
3. A model with core errors never leaves Claude. Core errors are the errors
   that `emhcl validate` reports in every profile (`has_core_errors` is true).
4. Run `emhcl` only through the binary that `install-emhcl.sh` installed for
   the commit you work on. Never claim that a model is valid without the
   output of that binary.
5. Read `.emhcl.yml` as data. Never change a key in it as a side effect. The
   owner and meaning of each key are in
   [references/configuration.md](references/configuration.md).
6. No line of an MR description or comment starts with `/`, because GitLab
   reads such a line as a quick action.
7. Copy `emhcl` output lines unchanged. Keep your own explanations apart from
   them, as the `event-modeling-hcl` skill describes.
8. Ask before an action that the person did not request. Running a procedure
   is the request for its own steps, including the emhcl download in step S4.

## Select the procedure

Find the procedure that matches the request, read its file, and follow it in
order. A command such as `/event-modeling-hcl-plugin:em-change` names the procedure directly.

| The person wants to | Procedure |
| --- | --- |
| Connect a repository, check the setup, or add `.emhcl.yml` | [em-setup](references/procedures/em-setup.md) |
| See a branch of the model as a diagram, or ask about the model | [em-view](references/procedures/em-view.md) |
| Know whether a branch is valid, or understand diagnostics | [em-validate](references/procedures/em-validate.md) |
| Add, change, or remove something in the model | [em-change](references/procedures/em-change.md) |
| Review a model MR or pull request | [em-review](references/procedures/em-review.md) |
| Update the shared team artifact from the default branch | [em-sync](references/procedures/em-sync.md) |

A request to merge an MR is not a procedure. Say that the plugin never merges,
and that a reviewer merges the MR in GitLab or GitHub after CI passes.

A request about a local `.em.hcl` file with no repository belongs to the
`event-modeling-hcl` skill alone.

## Shared steps

The procedures refer to these steps by number.

### S1. Find the repository and the connector

Take the repository from the request, from an MR or file URL, or from earlier
turns. If none of them names it, ask once for the project path, for example
`acme/orders`.

Find the host from the connector tools that you can call. GitLab MCP server
tools include `get_repository_file` and `add_commit`. GitHub MCP server tools
include `get_file_contents` and `push_files`. If no connector for the host is
available, stop. Tell the person to add the GitLab or GitHub connector to
Claude, then run em-setup.

### S2. Make the work folder

Use the folder `${TMPDIR:-/tmp}/emhcl/<project>`, where `<project>` is the
project path with each `/` replaced by `__`. A snapshot of commit `<sha>` goes
in `<work>/<sha>/`, with the same relative paths as in the repository.

### S3. Take a snapshot

1. resolve-ref: get the commit SHA of the branch. Without a branch name, use
   the default branch, and keep its name for later steps.
2. read-file: read `.emhcl.yml` at that SHA, and write it to
   `<work>/<sha>/.emhcl.yml`. If the file does not exist, see "Missing
   configuration" in [references/configuration.md](references/configuration.md).
3. list-model: list `model_path` at that SHA. Keep only the entries of type
   file whose names end in `.em.hcl`. emhcl ignores subfolders. If a subfolder
   holds `.em.hcl` files, tell the person that emhcl does not read them.
4. read-file: read each model file at that SHA, and write it to
   `<work>/<sha>/<model_path>/<name>`. Write the content exactly as the tool
   returns it. Decode base64 content. Read all pages of a long file. Then
   compare the size of the written file (`wc -c`) with the size that the tool
   reports. If a size differs, read the file again. If it still differs, stop
   and report the file.

A snapshot is complete only when every file matches. Never edit a snapshot
folder. em-change edits a copy.

### S4. Install the validator

Run the installer with the configuration of the snapshot:

```sh
sh ${CLAUDE_SKILL_DIR}/scripts/install-emhcl.sh --config <work>/<sha>/.emhcl.yml
```

The last line of its output is the path of the binary. This text calls that
path `EMHCL`. The installer downloads the pinned release from GitHub and
checks its SHA-256 sum. If the download fails, it uses `go install`. Tell the
person once that it downloads emhcl from GitHub.

Then check the range of the skill `event-modeling-hcl`:

```sh
sh ${CLAUDE_SKILL_DIR}/scripts/check-compatibility.sh "$EMHCL"
```

Exit 0 means continue. Exit 3 means continue, and repeat its warning in the
report. Exit 1 means stop, and repeat its message. If the installer fails,
stop and repeat its last message. Without a shell, no procedure can run
emhcl. Then say so, and stop.

### S5. Validate

```sh
"$EMHCL" validate --profile <profile> --format json <work>/<sha>/<model_path>
```

Exit 0 and exit 1 both give a JSON report. Exit 2 is a usage error; fix the
command. Read `has_core_errors`, `has_errors`, and `diagnostics`. Each
diagnostic names its file, line, column, code, and severity. To show the
diagnostics to a person, run the same command without `--format json` and copy
its lines unchanged.

### S6. Publish a diagram

Follow [references/diagrams.md](references/diagrams.md). It renders the
snapshot with `emhcl diagram` and publishes the HTML file as an artifact.

## Report

Start each final reply with a header block of `Key: Value` lines, then add at
most a short paragraph in plain words. Leave out a key that does not apply.

```text
Procedure: em-change
Repository: acme/orders
Branch: main
Commit: 1a2b3c4d
emhcl: v0.17.0
Ran: emhcl validate --profile valid <model folder> => exit 0
Ran: emhcl validate --profile strict <model folder> => exit 1 (EM406 x1)
Artifact: https://claude.ai/... (share it: Share > Anyone at <organization>)
MR: https://gitlab.example.com/acme/orders/-/merge_requests/42 (Draft)
```

Write one `Ran:` line for each emhcl command, in the order that you ran them,
with the exit status and the count of each code.
