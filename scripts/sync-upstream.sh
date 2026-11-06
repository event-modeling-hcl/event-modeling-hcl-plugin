#!/bin/sh
# sync-upstream.sh copies the pet-clinic folder model at one emhcl release tag,
# and writes the compatibility range of the skill event-modeling-hcl (DP2).
#
# Usage: scripts/sync-upstream.sh [--check] <tag>      for example v0.17.0
#
# The skill event-modeling-hcl lives in plugins/emhcl-skills. Its front matter
# names spec_version and emhcl_min. The tag is the newest emhcl release that
# the plugins were tested with (emhcl_max_tested).
#
# Without --check, the script replaces:
#   examples/pet-clinic/model/*.em.hcl             the upstream folder model
#   plugins/emhcl/skills/em-collaborate/references/compatibility.md
# and sets emhcl_version in examples/pet-clinic/.emhcl.yml to the tag.
#
# With --check, the script changes nothing. It exits 1 when any of those files
# differs from what the tag and the skill give. When EMHCL names an emhcl
# binary, it also exits 1 when the spec_version of the skill differs from the
# spec that the binary implements.
#
# Environment:
#   UPSTREAM_REPO  local clone of eventmodeling-hcl; the script then runs
#                  git archive in it instead of a download from GitHub
#   EMHCL          optional emhcl binary for the spec check
#
# Exit status: 0 done or equal, 1 failure or difference, 2 usage error.
set -eu

check=0
if [ "${1:-}" = --check ]; then
	check=1
	shift
fi
[ $# -eq 1 ] || {
	echo "usage: scripts/sync-upstream.sh [--check] <tag>" >&2
	exit 2
}
tag=$1
case $tag in
v[0-9]*.[0-9]*.[0-9]*) ;;
*)
	echo "sync-upstream: the tag must look like v0.17.0, not $tag" >&2
	exit 2
	;;
esac
version=${tag#v}

root=$(cd "$(dirname "$0")/.." && pwd)
skill_md=$root/plugins/emhcl-skills/skills/event-modeling-hcl/SKILL.md
compat=$root/plugins/emhcl/skills/em-collaborate/references/compatibility.md
example=$root/examples/pet-clinic

# front KEY reads one metadata value from the front matter of the skill.
front() {
	sed -n "s/^[[:space:]]*$1:[[:space:]]*\"\{0,1\}\([^\"]*\)\"\{0,1\}[[:space:]]*$/\1/p" "$skill_md" | head -n 1
}
skill_version=$(front version)
spec_version=$(front spec_version)
emhcl_min=$(front emhcl_min)
emhcl_min=${emhcl_min#v}
[ -n "$skill_version" ] && [ -n "$spec_version" ] && [ -n "$emhcl_min" ] || {
	echo "sync-upstream: $skill_md has no metadata version, spec_version, or emhcl_min" >&2
	exit 1
}

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT INT TERM
mkdir "$tmp/src"
if [ -n "${UPSTREAM_REPO:-}" ]; then
	git -C "$UPSTREAM_REPO" archive --format=tar "$tag" examples/pet-clinic | tar -xf - -C "$tmp/src"
else
	curl -fsSL "https://codeload.github.com/event-modeling-hcl/eventmodeling-hcl/tar.gz/refs/tags/$tag" |
		tar -xzf - -C "$tmp/src" --strip-components=1
fi
model_src=$tmp/src/examples/pet-clinic
ls "$model_src"/*.em.hcl >/dev/null 2>&1 || {
	echo "sync-upstream: $tag has no examples/pet-clinic/*.em.hcl" >&2
	exit 1
}

cat >"$tmp/compatibility.md" <<EOF
# Compatibility

The script \`scripts/sync-upstream.sh\` writes this file. Do not edit it by
hand.

The skill \`event-modeling-hcl\` of the plugin \`emhcl-skills\` supports each
emhcl release from \`emhcl_min\` on. The plugin release was tested with
\`emhcl_max_tested\`, which is also the tag of the example model. The script
\`check-compatibility.sh\` reads these keys.

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
	cmp -s "$tmp/compatibility.md" "$compat" || {
		echo "sync-upstream: $compat differs from $tag and the skill" >&2
		status=1
	}
	for f in "$model_src"/*.em.hcl; do
		cmp -s "$f" "$example/model/$(basename "$f")" || {
			echo "sync-upstream: examples/pet-clinic/model/$(basename "$f") differs from $tag" >&2
			status=1
		}
	done
	extra=$(cd "$example/model" && for f in *.em.hcl; do [ -f "$model_src/$f" ] || echo "$f"; done)
	[ -z "$extra" ] || {
		echo "sync-upstream: examples/pet-clinic/model has files that $tag does not have: $extra" >&2
		status=1
	}
	grep -q "^emhcl_version: $version\([[:space:]]\|$\)" "$example/.emhcl.yml" || {
		echo "sync-upstream: examples/pet-clinic/.emhcl.yml does not pin $version" >&2
		status=1
	}
	if [ -n "${EMHCL:-}" ]; then
		tool_spec=$("$EMHCL" version --format json | sed -n 's/.*"spec":[[:space:]]*"\([^"]*\)".*/\1/p')
		[ "$tool_spec" = "$spec_version" ] || {
			echo "sync-upstream: the skill targets $spec_version, but $EMHCL implements ${tool_spec:-an unknown spec}" >&2
			status=1
		}
	fi
	[ $status -eq 0 ] && echo "sync-upstream: the example and compatibility.md equal $tag"
	exit $status
fi

cp "$tmp/compatibility.md" "$compat"
mkdir -p "$example/model"
rm -f "$example/model"/*.em.hcl
cp "$model_src"/*.em.hcl "$example/model/"
sed "s/^emhcl_version:[^#]*/emhcl_version: $version            /" "$example/.emhcl.yml" >"$tmp/emhcl.yml"
cp "$tmp/emhcl.yml" "$example/.emhcl.yml"
echo "sync-upstream: copied the example from $tag, and wrote the range of skill $skill_version (spec $spec_version, emhcl $emhcl_min to $version)"
