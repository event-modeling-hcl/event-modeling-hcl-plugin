#!/usr/bin/env python3
"""Build standalone Codex skills from the canonical method and collaboration sources."""
import argparse
import os
from pathlib import Path, PurePosixPath
import re
import runpy


ROOT = Path(__file__).resolve().parents[1]
METHOD = Path("plugins/emhcl-skills/skills")
COLLABORATE = Path("plugins/emhcl/skills/em-collaborate")


def replace(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"Canonical platform adaptation no longer matches: {old[:100]!r}")
    return text.replace(old, new, 1)


def replace_section(text, heading, end, content):
    start = text.index(heading)
    finish = text.index(end, start) if end else len(text)
    return text[:start] + heading + "\n\n" + content.rstrip() + "\n\n" + text[finish:]


def adapt_skill(text):
    text = replace(text, "allowed-tools:\n  - Bash(sh ${CLAUDE_SKILL_DIR}/scripts/install-emhcl.sh *)\n  - Bash(sh ${CLAUDE_SKILL_DIR}/scripts/check-compatibility.sh *)\n", "")
    text = replace(text,
        "Needs the event-modeling-hcl skill of the plugin\n  event-modeling-skills. Claude Code installs this dependency automatically.\n  In chat and Cowork, install both plugins separately.",
        "Needs the sibling event-modeling-hcl skill installed with this package.\n  Runs locally in Codex CLI or IDE with shell access and configured MCP tools.")
    text = replace(text,
        "The language itself belongs to the skill `event-modeling-hcl` of the plugin\n`event-modeling-skills`. Claude Code installs that plugin as a dependency.\nIn chat and Cowork, install both plugins before running these procedures.",
        "The language itself belongs to the sibling skill `event-modeling-hcl`.\nThis standalone package installs it and all 32 method skills together.")
    text = replace(text, "A command such as `/event-modeling-hcl-plugin:em-change` names the procedure directly.",
        "Invoke `$em-collaborate` in Codex CLI or IDE, then name a procedure such as `em-change` in plain text.\nUse procedure names, not platform-prefixed slash commands.")
    text = replace(text,
        "Find the host from the connector tools that you can call.",
        "Find the host from the configured Codex MCP tools that you can call.\nMCP tool names may have a server prefix; match the operation and its schema,\nnot an assumed prefix. Use the seven-operation port below, not local Git or\n`gh`. A local checkout is not required. Discover configured tools before\nclaiming they are unavailable. Never invent a missing operation.\n\nFind the host from the connector tools that you can call.")
    text = replace(text, "### S4. Install the validator\n\nRun the installer", "### S4. Install the validator\n\n" + SCRIPT_LOCATION + "\nRun the installer")
    text = text.replace("${CLAUDE_SKILL_DIR}", "${EM_COLLABORATE_DIR}")
    text = text.replace('sh ${EM_COLLABORATE_DIR}/scripts/', 'sh "${EM_COLLABORATE_DIR}/scripts/').replace('install-emhcl.sh --config', 'install-emhcl.sh" --config').replace('check-compatibility.sh "$EMHCL"', 'check-compatibility.sh" "$EMHCL"')
    text = replace(text, "snapshot with `emhcl diagram` and publishes the HTML file as an artifact.",
        "snapshot with `emhcl diagram` and returns the unchanged local HTML file.\nCodex has no hosted artifact publisher; never describe this local file as a shared artifact.")
    text = replace(text, "Artifact: https://claude.ai/... (share it: Share > Anyone at <organization>)", "Artifact: none (Codex has no hosted artifact publisher)\nDiagram file: /absolute/path/to/diagram.html")
    text = text.replace("mirror the\n  default branch into a shared team artifact", "render the\n  default branch as a local HTML file (no hosted team-artifact updates)")
    text = text.replace("Update the shared team artifact from the default branch", "Render the default branch locally; report that hosted sync is unavailable")
    return text


SCRIPT_LOCATION = '''Locate scripts from the actual `em-collaborate/SKILL.md` that Codex loaded,
not from the working directory and not from a Claude environment variable.
The installed skill is normally under a project `.agents/skills` directory
or `~/.agents/skills`; an explicit installation may be elsewhere. Set the
absolute parent directory of that loaded file in your shell, for example:

```sh
EM_COLLABORATE_DIR='/absolute/path with spaces/.agents/skills/em-collaborate'
test -f "$EM_COLLABORATE_DIR/scripts/install-emhcl.sh"
test -f "$EM_COLLABORATE_DIR/scripts/check-compatibility.sh"
```

Replace the example path with the loaded skill's actual directory. Keep it
quoted in every command. Do not run a guessed script or an arbitrary script
found in the model repository. If the skill path cannot be established,
stop and report the missing installed package. Both scripts and their
relative `../references/compatibility.md` layout are shipped unchanged.
'''

DIAGRAM_DELIVERY = '''Codex CLI and IDE do not provide the Claude hosted-artifact publisher.
After rendering, return the unchanged HTML file's absolute local path and
report `Artifact: none (Codex has no hosted artifact publisher)`. Include
`Diagram file: <absolute path>` in the report. If the IDE can open a local
file, it is only a local preview, not a shareable team artifact.

Never rewrite, restyle, shorten, or retype the HTML. Never put a local path,
`file://` URL, or invented hosted URL in an MR description or comment as a
diagram link. Use the procedure's no-diagram-link alternative and explain
that the HTML is local. A person can share the file through their own
approved channel; do not claim to upload it or manage its permissions.

Ignore `team_artifact_url` for publishing on this surface. Read it as data
and leave it unchanged. Do not create a replacement URL, republish an
existing hosted artifact, or imply a local file mirrors that hosted artifact.
Name `canonical_url`, when configured, as the CI-maintained canonical view.

For em-sync, render only the default branch and explicitly report that the
shared team artifact was **not** updated. Do not issue Claude Share or
"Can edit" instructions. If a person supplies the text of a team-artifact
comment, use that text as an em-change request; do not pretend to fetch
hosted comments without an available tool.
'''


def adapt_collaboration(relative, text):
    if relative == "SKILL.md":
        text = adapt_skill(text)
    elif relative == "references/diagrams.md":
        text = replace(text, "The diagram publisher turns a snapshot folder into an artifact.",
                       "The Codex diagram adapter turns a snapshot folder into an unchanged local HTML file.")
        text = replace(text, "The team, inside Claude. Teammates comment on slices there.",
                       "Hosted team surface, unavailable for publishing from Codex.")
        text = replace_section(text, "## Publish", None, DIAGRAM_DELIVERY)
    elif relative == "references/procedures/em-sync.md":
        text = replace(text, "Republishes the team artifact from the default branch.",
                       "Renders the default branch locally. Codex cannot republish the hosted team artifact.")
        text = replace(text, "Composition: C(DP3 snapshot of the default branch → DP4 republish to\n`team_artifact_url`).",
                       "Composition: C(DP3 snapshot of the default branch → DP4 local HTML delivery).")
        start = text.index("3. Publish a diagram")
        end = text.index("## Report", start)
        text = text[:start] + '''3. Render and deliver the unchanged HTML file as
   [../diagrams.md](../diagrams.md) says, with the em-sync title.
   Codex cannot update or create a hosted team artifact. Whether
   `team_artifact_url` is set or empty, leave it and `.emhcl.yml` unchanged;
   never substitute a local path or invent a replacement URL. Report that
   the shared team artifact was not updated. em-sync writes nothing to Git.

''' + text[end:]
        text = replace(text, "when it is set, and say that the team artifact mirrors it.",
                       "when it is set. Include `Diagram file:` with the local path and say that\nthe shared team artifact was not updated.")
    elif relative == "references/configuration.md":
        text = replace(text, "The shared artifact that mirrors the default branch. em-sync republishes to it.",
                       "The shared artifact that mirrors the default branch on a hosted surface. Codex reads but never updates it; em-sync delivers local HTML only.")
    elif relative == "references/procedures/em-change.md":
        text = replace(text, "Report the error. The artifact stays private to\nthe author.",
                       "Report the error. The unchanged HTML remains a local file;\nno hosted artifact was created.")
    return text.replace("Claude", "Codex")


def collect_files(fit=True):
    required = [METHOD, COLLABORATE, Path("contract/method.md"), Path("contract/hcl-binding.md"),
                Path("plugins/emhcl-skills/NOTICE"), Path("LICENSE"), Path("scripts/install-codex.py"),
                Path("platforms/codex/README.md")]
    required.extend(COLLABORATE / path for path in (
        "SKILL.md", "scripts/install-emhcl.sh", "scripts/check-compatibility.sh",
        "references/compatibility.md", "references/configuration.md",
        "references/diagrams.md", "references/git-operations.md"))
    required.extend(COLLABORATE / f"references/procedures/{name}.md" for name in (
        "em-setup", "em-view", "em-validate", "em-change", "em-review", "em-sync"))
    for relative in required:
        if not (ROOT / relative).exists():
            raise ValueError(f"Missing canonical package source: {relative}")
    skills = sorted((ROOT / METHOD).iterdir())
    if len(skills) != 33 or any(not (skill / "SKILL.md").is_file() for skill in skills):
        raise ValueError("Expected all 33 canonical method/language skills")
    files = {}
    for source, prefix in [(ROOT / METHOD, "skills"), (ROOT / COLLABORATE, "skills/em-collaborate")]:
        for path in sorted(source.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Canonical source must not be a symlink: {path}")
            if not path.is_file():
                continue
            relative = path.relative_to(source).as_posix()
            content = path.read_bytes()
            if source == ROOT / COLLABORATE and path.suffix == ".md":
                content = adapt_collaboration(relative, content.decode("utf-8")).encode()
            if path.name == "SKILL.md":
                content += b'\n## Package provenance\n\nSee [source and license notices](../.emhcl-codex/provenance.md).\n'
            files[f"{prefix}/{relative}"] = content
    for relative in ("contract/method.md", "contract/hcl-binding.md", "LICENSE"):
        files[f"skills/.emhcl-codex/{relative}"] = (ROOT / relative).read_bytes()
    files["skills/.emhcl-codex/NOTICE"] = (ROOT / "plugins/emhcl-skills/NOTICE").read_bytes()
    files["skills/.emhcl-codex/provenance.md"] = b'''# Source and license notices

Generated from the canonical `plugins/emhcl-skills/skills` (33 method/language
skills), `plugins/emhcl/skills/em-collaborate` (six collaboration procedures),
and `contract/` in event-modeling-hcl/event-modeling-hcl-plugin.
The Codex adapter changes discovery, tool naming, invocation, script paths,
and diagram delivery only; it does not define a separate modeling method.

See the [repository license](LICENSE) and the unchanged
[source and methodology notices](NOTICE).
The method skills use this project's original wording under Apache-2.0.
The notices credit the methodology and upstream language content without
claiming that third-party methodology articles use the same license.

[Method authority](contract/method.md) and
[HCL binding authority](contract/hcl-binding.md) are included for provenance.
Use each skill's local references for its applicable rules.
'''
    files["install-codex.py"] = (ROOT / "scripts/install-codex.py").read_bytes()
    files["README.md"] = (ROOT / "platforms/codex/README.md").read_bytes()
    if fit:
        fit_skills(files)
    validate_references(files)
    return files


# Codex CLI 0.162.1 truncates an explicitly invoked SKILL.md above about 8,000 bytes.
SKILL_LIMIT = 8000
CONTINUATION = "instructions-continued.md"
PACKAGE_SECTIONS = "\n## Package provenance\n"


def split_sections(text):
    """Split Markdown before each level-2 heading outside fenced code."""
    sections, fence = [""], None
    for line in text.splitlines(keepends=True):
        marker = line.lstrip()[:3]
        if marker in ("```", "~~~"):
            fence = None if fence == marker else fence or marker
        elif fence is None and line.startswith("## "):
            sections.append("")
        sections[-1] += line
    return sections


def fit_skills(files):
    """Move whole trailing sections of a long SKILL.md into a linked sibling file.

    The package sections stay in SKILL.md, so the runtime rules survive host truncation.
    """
    for name in [name for name in files if name.endswith("/SKILL.md")]:
        if len(files[name]) <= SKILL_LIMIT:
            continue
        body, marker, tail = files[name].decode("utf-8").partition(PACKAGE_SECTIONS)
        if not marker:
            raise ValueError(f"Missing package sections in {name}")
        sections = split_sections(body)
        for keep in range(len(sections) - 1, 0, -1):
            moved = sections[keep:]
            pointer = ("## Continue reading\n\nThis skill continues in "
                       f"[the remaining instructions]({CONTINUATION}).\n"
                       "Read that file completely before you act. It contains these sections:\n\n"
                       + "".join(f"- {section.splitlines()[0][3:]}\n" for section in moved))
            head = "".join(sections[:keep]).rstrip("\n") + "\n\n" + pointer + marker + tail
            if len(head.encode("utf-8")) <= SKILL_LIMIT:
                break
        else:
            raise ValueError(f"{name} cannot fit {SKILL_LIMIT} bytes at a section boundary")
        skill = PurePosixPath(name).parent
        files[name] = head.encode("utf-8")
        files[str(skill / CONTINUATION)] = (
            f"# {skill.name}: remaining instructions\n\n"
            "These sections continue [SKILL.md](SKILL.md) in their original order.\n\n"
            + "".join(moved).rstrip("\n") + "\n").encode("utf-8")



def validate_references(files):
    for name, content in files.items():
        if not name.startswith("skills/") or not name.endswith(".md"):
            continue
        text = content.decode("utf-8")
        if "${CLAUDE_SKILL_DIR}" in text or "allowed-tools:" in text:
            raise ValueError(f"Unadapted Claude skill assumption in {name}")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            target = target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            joined = os.path.normpath(str(PurePosixPath(name).parent / target))
            if joined not in files:
                raise ValueError(f"Missing standalone reference: {name} -> {target}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/codex", metavar="DIRECTORY",
                        help="Package directory (default: repository dist/codex)")
    args = parser.parse_args()
    try:
        output = Path(os.path.abspath(args.output.expanduser()))
        # Never allow a package build to overlap its own canonical inputs.
        protected = [ROOT / name for name in ("plugins", "contract", "scripts", "platforms", "tests", ".github", "ci-templates")]
        if output == ROOT or output in ROOT.parents or any(
                output == path or path in output.parents or output in path.parents for path in protected):
            raise ValueError("Output would overlap the repository or canonical source tree")
        files = collect_files()
        installer = runpy.run_path(str(ROOT / "scripts/install-codex.py"))
        installer["publish"](output, files, installer["PACKAGE_MANIFEST"], update=True)
    except (OSError, ValueError) as error:
        parser.exit(1, f"build-codex: {error}\n")
    print(f"Built 34 standalone Codex skills in {output}")
    print(f'Install: python3 "{output / "install-codex.py"}" --project /path/to/project')


if __name__ == "__main__":
    main()
