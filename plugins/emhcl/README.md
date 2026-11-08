# Event Modeling HCL Plugin

Release 0.1.0 provides team procedures for Event Modeling HCL files in GitLab or GitHub.
Diagnostics are reports of errors or warnings.
Claude can show a model, explain diagnostics, propose changes, review proposals, and refresh a shared diagram.

A review request holds proposed changes for human review.
GitLab calls this a merge request.
GitHub calls this a pull request.
The plugin never merges a request or writes to the default branch.

## Install and use

In Claude Code, run these commands to add the marketplace and install the collaboration plugin:

```sh
claude plugin marketplace add event-modeling-hcl/event-modeling-hcl-plugin
claude plugin install event-modeling-hcl-plugin@event-modeling-hcl
```

A plugin dependency is another plugin that it requires.
Claude Code also installs the required `event-modeling-skills` plugin through the declared dependency.
In Claude chat and Cowork, install `event-modeling-skills` and `event-modeling-hcl-plugin` separately.
Automatic plugin dependencies work only in Claude Code.

For Claude chat, prepare and upload the plugins:

1. Download this repository.
2. Create a separate ZIP archive for each plugin folder.
   Use `plugins/emhcl/` for this plugin.
   Use `plugins/emhcl-skills/` for its required skills.
   Each ZIP must contain `.claude-plugin/plugin.json` at its root or inside one top-level folder.
3. In Claude chat, open Customize > Plugins > Add > Upload plugin.
4. Upload each ZIP through that control.

For Cowork, install both plugins separately through the available plugin controls.
See the [Claude installation guide](https://claude.com/docs/plugins/build#test-the-plugin-on-each-surface) for app instructions and organization controls.

A Git connector gives Claude access to your Git host.
Before you use a procedure, connect the GitLab or GitHub connector.
In Cowork and Claude Code, run `/event-modeling-hcl-plugin:em-setup` with your repository name.
In Claude chat, ask Claude to set up the repository in plain words.
Other requests can show the model, find errors, change it, review it, or update its shared diagram.
The command files provide `em-view`, `em-validate`, `em-change`, `em-review`, and `em-sync`.

## Requirements and program download

Every collaboration procedure needs a shell, a supported Git connector, and the `event-modeling-skills` plugin.
A shell runs commands in the execution environment.
GitLab changes need GitLab 19.4 or later.
The repository needs `.emhcl.yml`, which records the model folder and the emhcl version.
The setup procedure can propose this file through a review request when it is missing.
See the [configuration reference](skills/em-collaborate/references/configuration.md).

The plugins target specification v0.8.0 and need emhcl v0.17.0 or newer.
A pinned release is a specific version selected for use.
The [installer](skills/em-collaborate/scripts/install-emhcl.sh) uses the release pinned in `.emhcl.yml`.

It downloads the program and checksum file from GitHub with `curl` or `wget`.
A checksum is a value used to detect file changes.
Before installation, the installer makes sure that the SHA-256 checksum matches the downloaded program.

The download path also needs an archive extractor and `sha256sum` or `shasum`.
An archive extractor unpacks downloaded files.

If the download fails or no release archive exists for the platform, the installer tries `go install` at the same tag.
A fallback is an alternative when the first method fails.
The Go fallback needs Go and network access to its module sources.

A checksum mismatch stops installation without the Go fallback.
The installer writes to `$HOME/.local/bin` unless its configuration selects another folder.
Without a shell or a working installer, the collaboration procedure stops.

## Data and writes

Claude reads repository references, `.emhcl.yml`, model files, and review request details through your connected Git host.
Those contents enter the Claude session for the requested work.
A snapshot is a copy of the model files.
The procedures write model snapshots and generated diagrams under `${TMPDIR:-/tmp}/emhcl/<project>` in the execution environment.
The validator reads those local model files to find errors.
Program installation sends download requests to GitHub or Go module sources.

A change sends edited files, a commit message, and a review request to your connected Git host.
A review sends a comment to the existing request.
Setup can send a proposed configuration file through a new branch and review request.

An artifact is a file that Claude can display and share.
If the app supports artifact publication, the diagram procedure sends the generated HTML to Claude artifacts.
Do not provide repository content that your Claude or Git host policies prohibit.

## Diagrams and sharing

Artifact publication depends on the app and its available tools.
The plugin does not publish diagrams larger than 16 MiB as artifacts.
If publication is unavailable, it returns the generated HTML file and reports that no artifact exists.
It does not replace the diagram with a handmade page.

New artifacts are private until you share them through Claude.
Claude cannot change their access permissions.
See the [diagram reference](skills/em-collaborate/references/diagrams.md) for publication and sharing rules.

## License and attribution

This project work uses the [Apache License, Version 2.0](LICENSE).
Event Modeling is a methodology by Adam Dymitruk at Adaptech Group.
This project also credits [Martin Dilger](https://github.com/dilgerma).
See [Event Modeling](https://eventmodeling.org/) and [What is Event Modeling?](https://eventmodeling.org/posts/what-is-event-modeling/).
These links credit the methodology and do not assign a license to those articles.

They do not imply endorsement.
The required skills package includes its own license and attribution notice.

The [repository](https://github.com/event-modeling-hcl/event-modeling-hcl-plugin) contains shared setup instructions and CI templates.
CI runs automated tasks when repository changes occur.
Read [Set up a model repository](https://github.com/event-modeling-hcl/event-modeling-hcl-plugin#set-up-a-model-repository) for the GitLab and GitHub CI include blocks.
Use the `v0.1.0` references from those blocks.
