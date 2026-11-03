#!/bin/sh
# sync-upstream-skill.sh copies the upstream event-modeling-hcl skill and the
# pet-clinic folder model at one emhcl release tag (DP2).
#
# Usage: scripts/sync-upstream-skill.sh [--check] <tag>      for example v0.16.0
#
# Without --check, the script replaces:
#   plugins/emhcl/skills/event-modeling-hcl/       the skill, unchanged
#   examples/pet-clinic/model/*.em.hcl             the upstream folder model
#   plugins/emhcl/skills/em-collaborate/references/compatibility.md
# and sets emhcl_version in examples/pet-clinic/.emhcl.yml to the tag.
#
# With --check, the script changes nothing. It exits 1 when any of those files
# differs from what the tag gives.
#
# Environment:
#   UPSTREAM_REPO  local clone of eventmodeling-hcl; the script then runs
#                  git archive in it instead of a download from GitHub
#
# Exit status: 0 done or equal, 1 failure or difference, 2 usage error.
set -eu

check=0
if [ "${1:-}" = --check ]; then
	check=1
	shift
fi
[ $# -eq 1 ] || {
	echo "usage: scripts/sync-upstream-skill.sh [--check] <tag>" >&2
	exit 2
}
tag=$1
case $tag in
v[0-9]*.[0-9]*.[0-9]*) ;;
*)
	echo "sync-upstream-skill: the tag must look like v0.16.0, not $tag" >&2
	exit 2
	;;
esac
version=${tag#v}

root=$(cd "$(dirname "$0")/.." && pwd)
skill_dst=$root/plugins/emhcl/skills/event-modeling-hcl
compat=$root/plugins/emhcl/skills/em-collaborate/references/compatibility.md
example=$root/examples/pet-clinic

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT INT TERM
mkdir "$tmp/src"
if [ -n "${UPSTREAM_REPO:-}" ]; then
	git -C "$UPSTREAM_REPO" archive --format=tar "$tag" | tar -xf - -C "$tmp/src"
else
	curl -fsSL "https://codeload.github.com/event-modeling-hcl/eventmodeling-hcl/tar.gz/refs/tags/$tag" |
		tar -xzf - -C "$tmp/src" --strip-components=1
fi
skill_src=$tmp/src/.agents/skills/event-modeling-hcl
model_src=$tmp/src/examples/pet-clinic
[ -f "$skill_src/SKILL.md" ] || {
	echo "sync-upstream-skill: $tag has no .agents/skills/event-modeling-hcl/SKILL.md" >&2
	exit 1
}

# front VALUE_KEY reads one metadata value from the front matter of the skill.
front() {
	sed -n "s/^[[:space:]]*$1:[[:space:]]*\"\{0,1\}\([^\"]*\)\"\{0,1\}[[:space:]]*$/\1/p" "$skill_src/SKILL.md" | head -n 1
}
skill_version=$(front version)
spec_version=$(front spec_version)
emhcl_min=$(front emhcl_min)
emhcl_min=${emhcl_min#v}
[ -n "$emhcl_min" ] || {
	echo "sync-upstream-skill: the skill at $tag has no metadata.emhcl_min" >&2
	exit 1
}

cat >"$tmp/compatibility.md" <<EOF
# Compatibility

The script \`scripts/sync-upstream-skill.sh\` writes this file when it copies
the upstream skill. Do not edit it by hand.

The vendored skill \`event-modeling-hcl\` comes from the upstream tag below. It
supports each emhcl release from \`emhcl_min\` on. The plugin release was tested
with \`emhcl_max_tested\`. The script \`check-compatibility.sh\` reads these keys.

\`\`\`text
upstream_tag: $tag
skill_version: $skill_version
spec_version: $spec_version
emhcl_min: $emhcl_min
emhcl_max_tested: $version
\`\`\`
EOF

if [ $check -eq 1 ]; then
	status=0
	diff -r "$skill_src" "$skill_dst" >&2 || status=1
	cmp -s "$tmp/compatibility.md" "$compat" || {
		echo "sync-upstream-skill: $compat differs from $tag" >&2
		status=1
	}
	for f in "$model_src"/*.em.hcl; do
		cmp -s "$f" "$example/model/$(basename "$f")" || {
			echo "sync-upstream-skill: examples/pet-clinic/model/$(basename "$f") differs from $tag" >&2
			status=1
		}
	done
	extra=$(cd "$example/model" && for f in *.em.hcl; do [ -f "$model_src/$f" ] || echo "$f"; done)
	[ -z "$extra" ] || {
		echo "sync-upstream-skill: examples/pet-clinic/model has files that $tag does not have: $extra" >&2
		status=1
	}
	grep -q "^emhcl_version: $version\([[:space:]]\|$\)" "$example/.emhcl.yml" || {
		echo "sync-upstream-skill: examples/pet-clinic/.emhcl.yml does not pin $version" >&2
		status=1
	}
	[ $status -eq 0 ] && echo "sync-upstream-skill: the vendored files equal $tag"
	exit $status
fi

rm -rf "$skill_dst"
cp -R "$skill_src" "$skill_dst"
cp "$tmp/compatibility.md" "$compat"
mkdir -p "$example/model"
rm -f "$example/model"/*.em.hcl
cp "$model_src"/*.em.hcl "$example/model/"
sed "s/^emhcl_version:[^#]*/emhcl_version: $version            /" "$example/.emhcl.yml" >"$tmp/emhcl.yml"
cp "$tmp/emhcl.yml" "$example/.emhcl.yml"
echo "sync-upstream-skill: copied the skill $skill_version (spec $spec_version, emhcl $emhcl_min or newer) from $tag"
