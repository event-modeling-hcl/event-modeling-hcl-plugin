#!/usr/bin/env python3
"""Install a built Codex package without overwriting foreign or edited files."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tempfile


PACKAGE_MANIFEST = ".emhcl-codex-package.json"
INSTALL_MANIFEST = ".emhcl-codex-install.json"
FORMAT = "emhcl-codex-1"


def digest(content):
    return hashlib.sha256(content).hexdigest()


def safe_root(path):
    path = Path(os.path.abspath(path.expanduser()))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f"Symlink destination is not supported: {part}")
        if part.exists() and not part.is_dir():
            raise ValueError(f"Destination parent is not a directory: {part}")
    if path == Path(path.anchor):
        raise ValueError("A filesystem root is not a package destination")
    return path


def validate_entries(entries):
    if not isinstance(entries, dict) or not entries:
        raise ValueError("Manifest has no file inventory")
    for name, checksum in entries.items():
        path = PurePosixPath(name)
        if (not name or path.is_absolute() or ".." in path.parts
                or str(path) != name or "\\" in name
                or not isinstance(checksum, str) or len(checksum) != 64
                or any(char not in "0123456789abcdef" for char in checksum)):
            raise ValueError(f"Invalid manifest entry: {name}")
    return entries


def read_manifest(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing regular manifest: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("format") != FORMAT:
        raise ValueError(f"Unrecognized package manifest: {path}")
    return validate_entries(data.get("files"))


def checked_path(root, name):
    path = root / name
    for part in (path, *path.parents):
        if part == root:
            break
        if part.is_symlink():
            raise ValueError(f"Symlink conflicts with package content: {part}")
    return path


def publish(root, files, manifest_name, update, exclusive_roots=()):
    """Preflight the whole update before changing any destination content."""
    root = safe_root(root)
    entries = {name: digest(data) for name, data in sorted(files.items())}
    validate_entries(entries)
    manifest_path = root / manifest_name
    exists = manifest_path.exists() or manifest_path.is_symlink()
    if exists and not update:
        raise ValueError("An installation already exists; use --update for an unmodified managed installation")
    previous = read_manifest(manifest_path) if exists else {}
    for name in exclusive_roots:
        directory = checked_path(root, name)
        if directory.exists() and not any(p.startswith(name + "/") for p in previous):
            raise ValueError(f"Refusing an existing unowned skill directory: {directory}")
    for name, checksum in previous.items():
        path = checked_path(root, name)
        if not path.is_file() or digest(path.read_bytes()) != checksum:
            raise ValueError(f"Managed file was changed or removed; preserve it before updating: {path}")
    for name in entries:
        path = checked_path(root, name)
        if path.exists() and name not in previous:
            raise ValueError(f"Refusing to overwrite unowned content: {path}")
        if path.exists() and not path.is_file():
            raise ValueError(f"File destination is not a regular file: {path}")
        for parent in path.parents:
            if parent == root:
                break
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"File parent is not a directory: {parent}")
    manifest = (json.dumps({"format": FORMAT, "files": entries}, indent=2, sort_keys=True) + "\n").encode()
    root.mkdir(parents=True, exist_ok=True)
    # Stage every new byte first; conflicts have already been rejected above.
    with tempfile.TemporaryDirectory(prefix=".emhcl-codex-stage-", dir=root) as temporary:
        stage = Path(temporary)
        for name, data in files.items():
            path = stage / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (stage / manifest_name).write_bytes(manifest)
        for name in files:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            os.replace(stage / name, path)
        for name in previous.keys() - entries.keys():
            (root / name).unlink()
        os.replace(stage / manifest_name, manifest_path)
    return root


def package_files(source):
    source = source.expanduser().resolve()
    entries = read_manifest(source / PACKAGE_MANIFEST)
    files = {}
    for name, checksum in entries.items():
        path = checked_path(source, name)
        if not path.is_file() or digest(path.read_bytes()) != checksum:
            raise ValueError(f"Package is incomplete or modified; rebuild it: {path}")
        if name.startswith("skills/"):
            files[name[len("skills/"):]] = path.read_bytes()
    if not files or "em-collaborate/SKILL.md" not in files:
        raise ValueError("Package has no collaboration skill")
    actual = {str(p.relative_to(source / "skills")) for p in (source / "skills").rglob("*")
              if p.is_file() or p.is_symlink()}
    if actual != set(files):
        raise ValueError("Package skill inventory differs from its manifest; rebuild it")
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    adjacent = Path(__file__).resolve().parent
    default_source = adjacent if (adjacent / "skills").is_dir() else adjacent.parent / "dist/codex"
    parser.add_argument("--source", type=Path, default=default_source,
                        metavar="PACKAGE", help="Built package (default: adjacent package or repository dist/codex)")
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--project", type=Path, metavar="DIRECTORY",
                        help="Install into DIRECTORY/.agents/skills")
    choice.add_argument("--user", action="store_true", help="Install into ~/.agents/skills")
    choice.add_argument("--destination", type=Path, metavar="DIRECTORY", help="Explicit skills directory")
    parser.add_argument("--update", action="store_true", help="Update only unchanged, previously managed files")
    args = parser.parse_args()
    target = (args.project / ".agents/skills" if args.project is not None else
              Path.home() / ".agents/skills" if args.user else args.destination)
    try:
        files = package_files(args.source)
        roots = sorted({name.split("/", 1)[0] for name in files})
        target = publish(target, files, INSTALL_MANIFEST, args.update, roots)
    except (OSError, ValueError) as error:
        parser.exit(1, f"install-codex: {error}\n")
    print(f"Installed 34 skills in {target}")
    print("In Codex CLI or IDE, invoke $em-collaborate then request em-setup, em-view, em-validate, em-change, em-review, or em-sync.")


if __name__ == "__main__":
    main()
