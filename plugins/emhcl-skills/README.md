# Event Modeling Skills

Release 0.1.0 contains 32 method skills and the `event-modeling-hcl` language skill.
The method skills discover business facts, build a model, review evidence, and plan delivery slices.
A delivery slice is a model part planned for implementation.

The language skill writes and reviews `.em.hcl` files for specification v0.8.0.
Business discussions do not require an HCL file or a command-line tool.

## Install and use

In Claude Code, run these commands to add the marketplace and install the skills plugin:

```sh
claude plugin marketplace add event-modeling-hcl/event-modeling-hcl-plugin
claude plugin install event-modeling-skills@event-modeling-hcl
```

For Claude chat, prepare and upload the skills plugin:

1. Download this repository.
2. Create a ZIP archive of the `plugins/emhcl-skills/` folder.
   The ZIP must contain `.claude-plugin/plugin.json` at its root or inside one top-level folder.
3. In Claude chat, open Customize > Plugins > Add > Upload plugin.
4. Upload the ZIP through that control.

In Cowork, install the skills plugin through the available plugin controls.
See the [Claude installation guide](https://claude.com/docs/plugins/build#test-the-plugin-on-each-surface) for app instructions and organization controls.

An event model describes business events and related actions.
A business event records something that happened in the business.
A command is a request to perform an action.
A scenario describes expected behavior for a specific case.

Ask Claude to build a complete event model, lead a workshop, or work on one model part.
For example, ask it to list business events or write scenarios for a command.
If you need the model in HCL, ask for `.em.hcl` files.
Diagnostics are reports of errors or warnings.
Use the [language skill](skills/event-modeling-hcl/SKILL.md) for syntax, formatting, migration, and diagnostic explanations.

For Git collaboration, also install `event-modeling-hcl-plugin` from this repository.
Claude Code installs these skills automatically when you install that collaboration plugin.
In Claude chat and Cowork, install both plugins separately.
A plugin dependency is another plugin that it requires.
Automatic plugin dependencies work only in Claude Code.
This skills package does not require the collaboration plugin for standalone modeling.

## Requirements and tool fallback

A shell runs commands in the Claude execution environment.
The method skills need the business information that you want Claude to model.
Machine validation uses emhcl to find errors in model files.
The language skill targets specification v0.8.0 and needs emhcl v0.17.0 or newer for machine validation.
It first looks for a compatible program in your repository or on `PATH`.
`PATH` lists the folders where the shell finds programs.

The language skill does not install a program or run an untrusted download without your request.
For an authorized installation, use the [upstream emhcl instructions](https://github.com/event-modeling-hcl/eventmodeling-hcl/tree/v0.17.0).
Program installation needs network access to the selected distribution source.

Running emhcl needs a shell.
A static language checklist guides review without running emhcl.
If no compatible program is available, Claude uses that checklist.
This review does not run machine validation.
It cannot establish that a model is valid or ready for implementation.
The language skill must report that limitation.

A fallback is an alternative when the first method fails.
The separate collaboration plugin downloads a specific GitHub release and uses Go installation as a fallback.
That installer is not part of this standalone skills package.

## Data and files

Claude reads the business descriptions, documents, source code, and model files that the requested task needs.
Those contents enter the Claude session under the data controls for your account.
The skills can write requested model files, scenarios, evidence references, and tool outputs in the execution environment.
Formatting, migration, and repair can change model files within the scope that you authorize.
Review-only requests do not authorize file changes.

The skills do not define a separate data service or a Git publication procedure.
When authorized, program installation sends download requests to the selected distribution source.
Local emhcl commands read model files and write their requested outputs.

A Git connector gives Claude access to your Git host.
The repository procedures in the collaboration plugin require both that plugin and a Git connector.
Do not supply content that your Claude or repository policies prohibit.

An artifact is a file that Claude can display and share.
These skills do not include a procedure for publishing artifacts.
Diagram sharing depends on the app and its available tools.
The collaboration plugin documents its artifact limits and provides an HTML file when artifact publication is unavailable.

## License and attribution

This project work uses the [Apache License, Version 2.0](LICENSE).
The author states that the method text uses original wording, not copied or adapted third-party method text.
The [NOTICE](NOTICE) credits Event Modeling by Adam Dymitruk at Adaptech Group and upstream emhcl v0.17.0 language content.
This project also credits [Martin Dilger](https://github.com/dilgerma).
The attribution does not assign a license to community articles or imply endorsement.
See the [repository](https://github.com/event-modeling-hcl/event-modeling-hcl-plugin) for shared setup instructions and release information.
