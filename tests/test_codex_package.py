"""Behavior checks for the standalone Codex package (Python standard library)."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build-codex.py"
INSTALLER = ROOT / "scripts/install-codex.py"


class CodexPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex package ")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name).resolve()
        self.package = self.work / "standalone package"

    def invoke(self, script, *args, ok=True, env=None):
        result = subprocess.run([sys.executable, str(script), *map(str, args)],
                                text=True, capture_output=True, env=env)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def build(self):
        self.invoke(BUILDER, "--output", self.package)
        return self.package

    def tree(self, root):
        return {str(p.relative_to(root)): p.read_bytes()
                for p in root.rglob("*") if p.is_file()}

    def test_all_skills_procedures_and_local_references_survive_standalone_copy(self):
        self.build()
        detached = self.work / "detached" / "package"
        shutil.copytree(self.package, detached)
        source_names = {p.parent.name for p in
                        (ROOT / "plugins/emhcl-skills/skills").glob("*/SKILL.md")}
        skills = detached / "skills"
        self.assertEqual({p.parent.name for p in skills.glob("*/SKILL.md")},
                         source_names | {"em-collaborate"})
        self.assertEqual(len(source_names), 33)
        self.assertEqual({p.stem for p in (skills / "em-collaborate/references/procedures").glob("*.md")},
                         {"em-setup", "em-view", "em-validate", "em-change", "em-review", "em-sync"})
        for skill in skills.glob("*/SKILL.md"):
            # Codex CLI 0.162.1 truncates an explicitly invoked SKILL.md above about 8,000 bytes.
            self.assertLessEqual(skill.stat().st_size, 8000, skill)
        for document in skills.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
                target = target.split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                self.assertTrue((document.parent / target).exists(),
                                f"{document.relative_to(skills)} -> {target}")
        provenance = skills / ".emhcl-codex"
        self.assertEqual((provenance / "LICENSE").read_bytes(),
                         (ROOT / "LICENSE").read_bytes())
        self.assertEqual((provenance / "NOTICE").read_bytes(),
                         (ROOT / "plugins/emhcl-skills/NOTICE").read_bytes())

    def test_standalone_installer_and_validator_scripts_work_with_spaces(self):
        self.build()
        detached = self.work / "detached package"
        shutil.copytree(self.package, detached)
        target = self.work / "project with spaces/.agents/skills"
        self.invoke(detached / "install-codex.py", "--destination", target)
        self.assertEqual(
            {p.parent.name for p in target.glob("*/SKILL.md")},
            {p.parent.name for p in (detached / "skills").glob("*/SKILL.md")})
        scripts = target / "em-collaborate/scripts"
        fake = self.work / "emhcl fake"
        fake.write_text('#!/bin/sh\nprintf "emhcl v0.17.0\\n"\n')
        fake.chmod(0o755)
        result = subprocess.run(["sh", str(scripts / "check-compatibility.sh"), str(fake)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        config = self.work / "missing pin.yml"
        config.write_text("model_path: model\n")
        result = subprocess.run(["sh", str(scripts / "install-emhcl.sh"), "--config", str(config)],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        config.write_text("emhcl_version: 0.17.0\n")
        cached = self.work / "cached validator directory"
        cached.mkdir()
        shutil.copy2(fake, cached / "emhcl")
        result = subprocess.run(
            ["sh", str(scripts / "install-emhcl.sh"), "--config", str(config),
             "--bin-dir", str(cached)], capture_output=True, text=True,
            env={**os.environ, "EMHCL_NO_GO": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(Path(result.stdout.strip()), cached / "emhcl")
        self.assertTrue((target / "event-modeling-hcl/references/language-v0.8.md").is_file())
        self.assertEqual((target / ".emhcl-codex/NOTICE").read_bytes(),
                         (ROOT / "plugins/emhcl-skills/NOTICE").read_bytes())
        self.assertEqual((target / ".emhcl-codex/LICENSE").read_bytes(),
                         (ROOT / "LICENSE").read_bytes())

    def test_build_is_repeatable_and_preserves_unrelated_files(self):
        self.build()
        before = self.tree(self.package)
        self.invoke(BUILDER, "--output", self.package)
        self.assertEqual(self.tree(self.package), before)
        unrelated = self.package / "personal.txt"
        unrelated.write_text("keep me")
        self.invoke(BUILDER, "--output", self.package)
        self.assertEqual(unrelated.read_text(), "keep me")

    def test_build_refuses_foreign_or_modified_collisions_without_partial_writes(self):
        collision = self.package / "skills/em-collaborate/SKILL.md"
        collision.parent.mkdir(parents=True)
        collision.write_text("mine")
        before = self.tree(self.package)
        self.invoke(BUILDER, "--output", self.package, ok=False)
        self.assertEqual(self.tree(self.package), before)
        shutil.rmtree(self.package)
        self.build()
        collision.write_text("locally edited")
        before = self.tree(self.package)
        self.invoke(BUILDER, "--output", self.package, ok=False)
        self.assertEqual(self.tree(self.package), before)

    def test_install_choices_update_and_collision_preflight(self):
        self.build()
        project = self.work / "a project"
        self.invoke(INSTALLER, "--source", self.package, "--project", project)
        target = project / ".agents/skills"
        unrelated = target / "my-other-skill/SKILL.md"
        unrelated.parent.mkdir()
        unrelated.write_text("user-owned")
        self.invoke(INSTALLER, "--source", self.package, "--project", project, ok=False)
        self.invoke(INSTALLER, "--source", self.package, "--project", project, "--update")
        self.assertEqual(unrelated.read_text(), "user-owned")
        managed = target / "event-modeling-hcl/SKILL.md"
        managed.write_text("edited")
        before = self.tree(target)
        self.invoke(INSTALLER, "--source", self.package, "--project", project, "--update", ok=False)
        self.assertEqual(self.tree(target), before)
        home = self.work / "isolated home"
        self.invoke(INSTALLER, "--source", self.package, "--user", env={**os.environ, "HOME": str(home)})
        self.assertTrue((home / ".agents/skills/em-collaborate/SKILL.md").is_file())
        self.invoke(INSTALLER, "--source", self.package, ok=False)
        self.invoke(INSTALLER, "--source", self.package, "--user", "--destination", target, ok=False)

    def test_installer_rejects_existing_skill_directory_even_without_file_collision(self):
        self.build()
        target = self.work / "skills"
        existing = target / "em-collaborate"
        existing.mkdir(parents=True)
        (existing / "personal.txt").write_text("mine")
        before = self.tree(target)
        self.invoke(INSTALLER, "--source", self.package, "--destination", target, ok=False)
        self.assertEqual(self.tree(target), before)

    def test_symlink_targets_and_source_tree_output_are_rejected(self):
        self.build()
        real = self.work / "real"
        real.mkdir()
        linked = self.work / "link"
        linked.symlink_to(real, target_is_directory=True)
        self.invoke(BUILDER, "--output", linked, ok=False)
        self.invoke(INSTALLER, "--source", self.package, "--destination", linked, ok=False)
        self.assertEqual(list(real.iterdir()), [])
        self.invoke(BUILDER, "--output", ROOT / "plugins/emhcl-skills", ok=False)

    def test_missing_sources_and_tampered_package_fail_before_installation(self):
        fixture = self.work / "incomplete source"
        (fixture / "scripts").mkdir(parents=True)
        shutil.copy2(BUILDER, fixture / "scripts/build-codex.py")
        self.invoke(fixture / "scripts/build-codex.py", "--output", self.package, ok=False)
        self.assertFalse(self.package.exists())
        self.build()
        (self.package / "skills/em-collaborate/scripts/check-compatibility.sh").unlink()
        target = self.work / "skills"
        self.invoke(INSTALLER, "--source", self.package, "--destination", target, ok=False)
        self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
