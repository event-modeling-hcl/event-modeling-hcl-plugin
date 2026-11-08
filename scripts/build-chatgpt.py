#!/usr/bin/env python3
"""Build a standalone portable skills plugin for ChatGPT and Codex."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import sys


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PROVENANCE = "skills/.emhcl-plugin"


class PackageError(Exception):
    """The source or destination cannot safely produce a plugin."""


SCRIPT_LOCATION = '''Locate `skills/em-collaborate/SKILL.md` in the installed plugin that the host loaded.
Use that file's absolute parent directory, not the working directory, a guessed
cache path, a project `.agents/skills` tree, or a Claude environment variable.
The host can install or copy the plugin outside the original build directory.
Set the actual loaded skill directory in your shell, for example:

```sh
EM_COLLABORATE_DIR='/absolute/installed plugin/skills/em-collaborate'
test -f "$EM_COLLABORATE_DIR/scripts/install-emhcl.sh"
test -f "$EM_COLLABORATE_DIR/scripts/check-compatibility.sh"
```

Replace the example with the actual installed path. Keep it quoted in every
command. If the host does not expose that path or the scripts, stop and report
the missing installed resource. Do not search the model repository for a
replacement script. The scripts and their relative compatibility reference
remain together in this package.
'''

RUNTIME = '''# Runtime preflight

This plugin packages skills and resources, not tools or credentials.
Read the applicable skill and its local references before acting.
Select this plugin in ChatGPT Work mode, or invoke `$event-modeling-hcl-plugin:em-collaborate` in Codex.
Then name one of the six procedures in plain text.

Before any collaboration procedure, discover the actual available tools.
Require a callable shell and configured, authenticated Git MCP tools.
Match the operations required by the selected procedure to
[the seven-operation Git port](../em-collaborate/references/git-operations.md).
Use the tool schemas, not an assumed server prefix.
If any required tool, authentication, or operation is unavailable, stop the procedure.
Name the missing requirement. Do not substitute local Git, `gh`, an advisory
procedure, invented tool output, or a successful gate.
Explicit user scope and choices override optional skill guidance.
Do not use optional guidance to expand the requested task.
Fixed permission, validation, and human-only merge constraints still apply.
This applies to em-setup, em-view, em-validate, em-change, em-review, and em-sync.
A plugin installation alone does not grant repository access or shell execution.

Never claim that you read a repository, ran a command, validated a model,
wrote a file, posted a comment, or created a branch without actual tool evidence.
A repository URL or local path in a message does not grant access.
When tools cannot read the model, request the complete relevant model members.
Do not call supplied files a fetched repository snapshot.

For HCL work without a callable compatible validator, report static findings only.
Report `Ran: none` and `Gate: none` when you did not run the required commands.
Keep user-supplied diagnostics separate under `User-supplied validation:`.
Record their command, version, profile, exit status, and model identity when supplied.
Quote diagnostics unchanged. Do not attribute supplied results to a new run.
A later model change makes earlier validation evidence stale.
Data Analysis or a downloadable draft does not establish a compatible validator.

The canonical procedure owns snapshot, permission, validation, and publication gates.
Missing tools do not relax those gates. Preserve K13 locks and human-only merges.
Never write to the default branch, merge, approve, or close a pull or merge request.

Return the unchanged local HTML from `emhcl diagram` when the procedure renders it.
This plugin does not provide a hosted-artifact publisher.
Do not invent a hosted URL or claim that a shared team artifact was updated.
'''

# Listing text for the Plugins Directory. Limits: displayName and shortDescription 30
# characters, defaultPrompt three prompts of 128 characters.
INTERFACE = {
    "displayName": "Event Modeling HCL",
    "shortDescription": "Model business events in HCL",
    "longDescription": (
        "Model business behavior as an event model and keep it in .em.hcl files in Git. "
        "The plugin has 32 method skills, the Event Modeling HCL language skill, and six team procedures. "
        "The procedures view, validate, change, review, and sync a model through reviewed merge requests. "
        "They need a shell and configured GitHub or GitLab MCP tools. "
        "The plugin does not include those tools, credentials, or a hosted service. "
        "A person must merge each change."),
    "category": "Productivity",
    "defaultPrompt": [
        "Help me model the business events of a customer order workflow.",
        "Explain the flow of this .em.hcl model in plain words.",
        "Run em-setup for my Event Modeling HCL model repository.",
    ],
}


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def adapt_runtime(text):
    """Change host wording only; the shared collector owns method and Git policy."""
    text = text.replace(".emhcl-codex", ".emhcl-plugin")
    text = re.sub(r"Codex(?: CLI (?:or|and) IDE)?", "ChatGPT Work mode or Codex", text)
    return text.replace(
        "Invoke `$em-collaborate` in ChatGPT Work mode or Codex, then name a procedure",
        "Select this plugin in ChatGPT Work mode, or invoke `$event-modeling-hcl-plugin:em-collaborate` "
        "in Codex, then name a procedure")


def build_files():
    collector = runpy.run_path(str(ROOT / "scripts/build-codex.py"))
    collected = collector["collect_files"](fit=False)
    files = {}
    for name, content in collected.items():
        if not name.startswith("skills/"):
            continue
        name = name.replace("skills/.emhcl-codex/", PROVENANCE + "/")
        if name.endswith(".md"):
            text = content.decode("utf-8")
            if name == "skills/em-collaborate/SKILL.md":
                location = collector["SCRIPT_LOCATION"].replace("Claude", "Codex")
                text = collector["replace"](text, location, SCRIPT_LOCATION)
            # Keep method rules intact; update only provenance and runtime references.
            if name.startswith("skills/em-collaborate/") or name == PROVENANCE + "/provenance.md":
                text = adapt_runtime(text)
            else:
                text = text.replace("../.emhcl-codex/provenance.md", "../.emhcl-plugin/provenance.md")
            if name.endswith("/SKILL.md"):
                text += ("\n## Execution boundary\n\n"
                         "Explicit user scope and choices take priority over optional guidance in this skill.\n"
                         "The fixed permission, validation, and human-only merge rules still apply.\n"
                         "Before claiming execution or repository access, read "
                         "[the runtime preflight](../.emhcl-plugin/runtime.md).\n"
                         "Apply it before any collaboration procedure or validator command.\n")
            content = text.encode("utf-8")
        files[name] = content
    files[PROVENANCE + "/runtime.md"] = RUNTIME.encode("utf-8")
    canonical_manifest = json.loads((ROOT / "plugins/emhcl/.claude-plugin/plugin.json").read_text())
    manifest = {"$schema": SCHEMA}
    for key in ("name", "version", "author", "homepage", "repository", "license", "keywords"):
        manifest[key] = canonical_manifest[key]
    manifest["description"] = (
        "Model business behavior and work with Event Modeling HCL. "
        "Repository changes use reviewed merge requests with configured Git MCP tools.")
    manifest["extensions"] = {"com.openai": {"interface": {
        **INTERFACE, "developerName": canonical_manifest["author"]["name"],
        "websiteURL": canonical_manifest["homepage"]}}}
    files["plugin.json"] = json_bytes(manifest)
    files["README.md"] = (ROOT / "platforms/chatgpt/README.md").read_bytes()
    files["LICENSE"] = (ROOT / "LICENSE").read_bytes()
    files["NOTICE"] = (ROOT / "plugins/emhcl-skills/NOTICE").read_bytes()
    sources = {ROOT / name for name in (
        "contract/method.md", "contract/hcl-binding.md", "LICENSE", "plugins/emhcl-skills/NOTICE",
        "plugins/emhcl/.claude-plugin/plugin.json", "platforms/chatgpt/README.md",
        "scripts/build-chatgpt.py", "scripts/build-codex.py")}
    for directory in ("plugins/emhcl-skills/skills", "plugins/emhcl/skills/em-collaborate"):
        sources.update(path for path in (ROOT / directory).rglob("*") if path.is_file())
    files["source-inventory.json"] = json_bytes({"sources": [
        {"path": path.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in sorted(sources)]})
    collector["fit_skills"](files)
    collector["validate_references"](files)
    # Validate the setup guide too, including links after a detached copy.
    for name, content in files.items():
        if not name.endswith(".md"):
            continue
        for target in re.findall(r"\]\(([^)\s]+)\)", content.decode("utf-8")):
            target = target.split("#", 1)[0]
            if not target or ":" in target:
                continue
            resolved = os.path.normpath(str(Path(name).parent / target))
            if resolved not in files:
                raise PackageError(f"Missing standalone reference: {name} -> {target}")
    return files


def check_destination(destination):
    # Inspect lexical components before resolve() can hide a symlink.
    for component in (destination, *destination.parents):
        if component.is_symlink():
            raise PackageError("Destination contains a symlink: " + str(component))
        if component.exists() and not component.is_dir():
            raise PackageError("Destination or parent is not a directory: " + str(component))
    destination = destination.resolve()
    if destination == ROOT or destination in ROOT.parents:
        raise PackageError("Destination is the repository root or its parent: " + str(destination))
    for name in ("contract", "plugins", "platforms", "scripts", "tests", "docs", "examples",
                 "ci-templates", ".agents", ".claude-plugin", ".github", ".git"):
        protected = ROOT / name
        if destination == protected or protected in destination.parents:
            raise PackageError("Destination is inside a source tree: " + str(destination))
    if destination.exists() and any(destination.iterdir()):
        raise PackageError("Destination is not empty; choose a fresh directory: " + str(destination))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/chatgpt", metavar="DIRECTORY",
                        help="absent or empty output directory (default: dist/chatgpt)")
    arguments = parser.parse_args(argv)
    destination = arguments.output.absolute()
    try:
        check_destination(destination)
        files = build_files()
        # All collection and reference checks finish before the first write.
        check_destination(destination)
        destination.mkdir(parents=True, exist_ok=True)
        for filename, content in sorted(files.items()):
            target = destination / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(content)
            if filename.endswith(".sh"):
                target.chmod(0o755)
    except (OSError, PackageError, ValueError, KeyError) as error:
        print("build-chatgpt: " + str(error), file=sys.stderr)
        return 1
    print(f"Built portable skills plugin: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
