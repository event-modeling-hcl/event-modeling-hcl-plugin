"""Consumer tests for the standalone portable ChatGPT and Codex plugin."""

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build-chatgpt.py"
METHOD = ROOT / "plugins/emhcl-skills/skills"
COLLAB = ROOT / "plugins/emhcl/skills/em-collaborate"


def temporary_directory(**kwargs):
    # macOS temporary roots can have symlinked parents, which the builder rejects.
    return tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve(), **kwargs)


def snapshot(directory):
    return {path.relative_to(directory).as_posix(): path.read_bytes()
            for path in directory.rglob("*") if path.is_file()}


class ChatGPTPackageTests(unittest.TestCase):
    def build(self, destination, cwd=ROOT):
        return subprocess.run([sys.executable, str(BUILDER), "--output", str(destination)],
                              cwd=cwd, capture_output=True, text=True)

    def require_package(self, destination):
        result = self.build(destination)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads((destination / "plugin.json").read_text())

    def test_manifest_and_marketplace_resolve_the_same_portable_plugin(self):
        with temporary_directory() as temporary:
            package = Path(temporary) / "plugin"
            manifest = self.require_package(package)
            canonical = json.loads((ROOT / "plugins/emhcl/.claude-plugin/plugin.json").read_text())
            self.assertEqual(manifest["$schema"],
                             "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
            for field in ("name", "version", "author", "homepage", "repository", "license", "keywords"):
                self.assertEqual(manifest[field], canonical[field], field)
            catalog = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
            self.assertEqual(catalog["name"], "event-modeling-hcl")
            self.assertEqual(len(catalog["plugins"]), 1)
            entry = catalog["plugins"][0]
            self.assertEqual(entry["name"], manifest["name"])
            self.assertEqual(entry["source"], {"source": "local", "path": "./dist/chatgpt"})
            self.assertEqual(entry["policy"], {"installation": "AVAILABLE", "authentication": "ON_INSTALL"})
            self.assertEqual(entry["category"], "Productivity")

    def test_root_skill_discovery_and_resource_boundaries_survive_detachment(self):
        with temporary_directory() as temporary:
            package = Path(temporary) / "plugin"
            self.require_package(package)
            expected = {path.parent.name for path in METHOD.glob("*/SKILL.md")} | {"em-collaborate"}
            discovered = {path.parent.name for path in (package / "skills").glob("*/SKILL.md")}
            self.assertEqual(len(discovered), 34)
            self.assertEqual(discovered, expected)
            for skill in discovered:
                text = (package / "skills" / skill / "SKILL.md").read_text()
                self.assertRegex(text, r"(?m)^name: " + re.escape(skill) + r"\s*$")
            for source, target in ((METHOD, package / "skills"),
                                   (COLLAB, package / "skills/em-collaborate")):
                for resource in source.rglob("*"):
                    if not resource.is_file():
                        continue
                    copied = target / resource.relative_to(source)
                    self.assertTrue(copied.is_file(), copied)
                    if source == METHOD and resource.name != "SKILL.md" or resource.suffix != ".md":
                        self.assertEqual(copied.read_bytes(), resource.read_bytes(), copied)
            provenance = package / "skills/.emhcl-plugin"
            for authority in ("method.md", "hcl-binding.md"):
                self.assertEqual((provenance / "contract" / authority).read_bytes(),
                                 (ROOT / "contract" / authority).read_bytes())
            self.assertEqual((package / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())
            self.assertEqual((package / "NOTICE").read_bytes(),
                             (ROOT / "plugins/emhcl-skills/NOTICE").read_bytes())
            for obsolete in ("knowledge", "instructions.txt", "manifest.json", "install-codex.py", ".codex-plugin"):
                self.assertFalse((package / obsolete).exists(), obsolete)
            self.assertFalse(any(path.is_symlink() for path in package.rglob("*")))

    def test_every_local_markdown_link_resolves_inside_the_package(self):
        with temporary_directory() as temporary:
            package = Path(temporary) / "plugin"
            self.require_package(package)
            for document in package.rglob("*.md"):
                for target in re.findall(r"\]\(([^)\s]+)\)", document.read_text()):
                    parsed = urlsplit(target)
                    if parsed.scheme or not parsed.path:
                        continue
                    resolved = (document.parent / unquote(parsed.path)).resolve()
                    self.assertTrue(resolved.is_relative_to(package.resolve()), (document, target))
                    self.assertTrue(resolved.exists(), (document, target))

    def test_explicitly_invoked_skills_fit_the_codex_limit_without_losing_text(self):
        # Codex CLI 0.162.1 truncates an explicitly invoked SKILL.md above about 8,000 bytes.
        with temporary_directory() as temporary:
            package = Path(temporary) / "plugin"
            self.require_package(package)
            split = 0
            for skill in (package / "skills").glob("*/SKILL.md"):
                text = skill.read_text()
                self.assertLessEqual(len(skill.read_bytes()), 8000, skill)
                self.assertIn("\n## Execution boundary\n", text, skill)
                continued = skill.parent / "instructions-continued.md"
                source = METHOD / skill.parent.name / "SKILL.md"
                if not continued.exists() or not source.exists():
                    continue
                split += 1
                head = text.split("\n## Continue reading\n", 1)[0].rstrip("\n")
                rest = continued.read_text().split("\n\n", 2)[2].rstrip("\n")
                self.assertEqual(head + "\n\n" + rest, source.read_text().rstrip("\n"), skill)
            self.assertGreater(split, 0)

    def test_source_inventory_hashes_identify_the_canonical_inputs(self):
        with temporary_directory() as temporary:
            package = Path(temporary) / "plugin"
            self.require_package(package)
            inventory = json.loads((package / "source-inventory.json").read_text())
            entries = {entry["path"]: entry["sha256"] for entry in inventory["sources"]}
            required = {path.relative_to(ROOT).as_posix() for source in (METHOD, COLLAB)
                        for path in source.rglob("*") if path.is_file()}
            required.update(("contract/method.md", "contract/hcl-binding.md", "LICENSE",
                             "plugins/emhcl-skills/NOTICE", "plugins/emhcl/.claude-plugin/plugin.json"))
            self.assertTrue(required <= entries.keys())
            for name, digest in entries.items():
                self.assertEqual(digest, hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), name)

    def test_builds_are_deterministic_and_independent_of_working_directory(self):
        with temporary_directory() as temporary:
            first, second = Path(temporary) / "first", Path(temporary) / "second"
            self.require_package(first)
            result = self.build(second, cwd=Path(temporary))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(snapshot(first), snapshot(second))

    def test_packaged_scripts_run_without_the_source_repository(self):
        with temporary_directory(prefix="emhcl plugin ") as temporary:
            package = Path(temporary) / "detached"
            self.require_package(package)
            scripts = package / "skills/em-collaborate/scripts"
            compatibility = subprocess.run([str(scripts / "check-compatibility.sh")],
                                           cwd=temporary, capture_output=True, text=True)
            self.assertEqual(compatibility.returncode, 2, compatibility.stderr)
            self.assertIn("usage:", compatibility.stderr)
            compatibility = subprocess.run(
                [str(scripts / "check-compatibility.sh"), sys.executable],
                cwd=temporary, capture_output=True, text=True)
            self.assertEqual(compatibility.returncode, 1, compatibility.stderr)
            self.assertIn("version failed", compatibility.stderr)
            config = Path(temporary) / ".emhcl.yml"
            config.write_text("model_path: model\n")
            binaries = Path(temporary) / "installed bin"
            result = subprocess.run([str(scripts / "install-emhcl.sh"), "--config", str(config),
                                     "--bin-dir", str(binaries)], cwd=temporary,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("has no emhcl_version", result.stderr)
            self.assertFalse(binaries.exists())

    def test_nonempty_file_and_rebuild_targets_are_unchanged(self):
        with temporary_directory() as temporary:
            directory = Path(temporary) / "nonempty"
            directory.mkdir()
            (directory / "sentinel").write_bytes(b"keep")
            before = snapshot(directory)
            self.assertNotEqual(self.build(directory).returncode, 0)
            self.assertEqual(snapshot(directory), before)
            file = Path(temporary) / "file"
            file.write_bytes(b"keep")
            self.assertNotEqual(self.build(file).returncode, 0)
            self.assertEqual(file.read_bytes(), b"keep")
            package = Path(temporary) / "built"
            self.require_package(package)
            before = snapshot(package)
            self.assertNotEqual(self.build(package).returncode, 0)
            self.assertEqual(snapshot(package), before)

    def test_symlink_destinations_and_parent_components_are_rejected_without_writes(self):
        with temporary_directory() as temporary:
            actual = Path(temporary) / "actual"
            actual.mkdir()
            link = Path(temporary) / "link"
            link.symlink_to(actual, target_is_directory=True)
            for destination in (link, link / "new" / "package"):
                self.assertNotEqual(self.build(destination).returncode, 0)
                self.assertEqual(snapshot(actual), {})
                self.assertEqual(list(actual.iterdir()), [])

    def test_repository_sources_and_ancestors_are_protected_before_writes(self):
        destinations = [ROOT, ROOT.parent, ROOT / "contract/native-output-must-not-exist",
                        ROOT / "plugins/emhcl-skills/skills/native-output-must-not-exist",
                        ROOT / "plugins/emhcl/skills/em-collaborate/native-output-must-not-exist",
                        ROOT / "platforms/chatgpt/native-output-must-not-exist",
                        ROOT / "scripts/native-output-must-not-exist",
                        ROOT / "tests/native-output-must-not-exist"]
        for destination in destinations:
            with self.subTest(destination=destination):
                existed = destination.exists()
                result = self.build(destination)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertEqual(destination.exists(), existed)

    def test_missing_sources_fail_before_creating_an_output_directory(self):
        with temporary_directory() as temporary:
            source = Path(temporary) / "incomplete"
            (source / "scripts").mkdir(parents=True)
            builder = source / "scripts/build-chatgpt.py"
            shutil.copy2(BUILDER, builder)
            destination = Path(temporary) / "output"
            result = subprocess.run([sys.executable, str(builder), "--output", str(destination)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(destination.exists())

    def test_existing_empty_destination_is_supported(self):
        with temporary_directory() as temporary:
            self.require_package(Path(temporary))


if __name__ == "__main__":
    unittest.main()
