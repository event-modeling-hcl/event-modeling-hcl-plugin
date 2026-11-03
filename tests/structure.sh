#!/bin/sh
# Structure tests of the plugin repository. They keep the zeros of the design
# matrix true. Run from any folder: sh tests/structure.sh
# The vendored skill check downloads the upstream tag (or uses UPSTREAM_REPO).
set -u

root=$(cd "$(dirname "$0")/.." && pwd)
plugin=$root/plugins/emhcl
skill=$plugin/skills/em-collaborate
failures=0
pass() { printf 'ok   %s\n' "$1"; }
fail() {
	printf 'FAIL %s\n' "$1"
	failures=$((failures + 1))
}

commands="em-setup em-view em-validate em-change em-review em-sync"

# Each command is a one-line entry point that names an existing procedure.
for c in $commands; do
	f=$plugin/commands/$c.md
	if [ -f "$f" ] && grep -q "procedure \`$c\` in \`references/procedures/$c.md\`" "$f" &&
		[ -f "$skill/references/procedures/$c.md" ]; then
		pass "command $c names an existing procedure"
	else fail "command $c names an existing procedure"; fi
done
extra=$(cd "$plugin/commands" && for f in *.md; do case " $commands " in *" ${f%.md} "*) ;; *) echo "$f" ;; esac; done)
[ -z "$extra" ] && pass "no command outside the six commands" || fail "unexpected commands: $extra"

# Each skill and command starts with front matter that has a description.
# (claude plugin validate does not catch a broken description.)
for f in "$plugin"/skills/*/SKILL.md "$plugin"/commands/*.md; do
	if [ "$(head -n 1 "$f")" = --- ] && sed -n '2,/^---$/p' "$f" | grep -q '^description:[[:space:]]*[^[:space:]]'; then
		:
	else fail "front matter with a description: ${f#"$root"/}"; fi
done
pass "front matter checked for each skill and command"

# FR1 and DP5: no CI template names an emhcl version.
# Plugin tags such as emhcl--v0.1.0 in the usage comments are not emhcl versions.
templates="$root/ci-templates/emhcl.gitlab-ci.yml $root/.github/workflows/emhcl-model.yml"
if grep -nE 'emhcl_version|[0-9]+\.[0-9]+\.[0-9]+|eventmodeling-hcl/releases|cmd/emhcl@' $templates | grep -v 'emhcl--v'; then
	fail "a CI template names an emhcl version"
else pass "no CI template names an emhcl version"; fi

# DP1: only install-emhcl.sh reads emhcl_version. Other code only writes or documents it.
readers=$(grep -rlE 'sed[^|]*emhcl_version' "$root" --include='*.sh' --include='*.yml' | grep -v -e '/install-emhcl.sh$' -e '/sync-upstream-skill.sh$' -e '/tests/')
[ -z "$readers" ] && pass "only install-emhcl.sh reads emhcl_version" || fail "other readers of emhcl_version: $readers"

# Each key of an example configuration carries one owner tag.
for cfg in "$root/examples/pet-clinic/.emhcl.yml"; do
	bad=$(grep -vE '^#|^$' "$cfg" | grep -vE '# \[(DP1|DP3|DP4|DP5|commands)\]' || true)
	[ -z "$bad" ] && pass "each key of $(basename "$(dirname "$cfg")")/.emhcl.yml has one owner" || fail "keys without an owner: $bad"
done

# The marketplace entry and the manifest agree on the plugin name.
if grep -q '"name": "emhcl"' "$root/.claude-plugin/marketplace.json" && grep -q '"name": "emhcl"' "$plugin/.claude-plugin/plugin.json"; then
	pass "marketplace entry and manifest name agree"
else fail "marketplace entry and manifest name agree"; fi

# The procedures never name a merge tool except to forbid it.
if grep -rn 'accept_merge_request\|merge_pull_request' "$skill/references/procedures"; then
	fail "a procedure names a merge tool"
else pass "no procedure names a merge tool"; fi

# The vendored skill, the example model, and compatibility.md equal the upstream tag.
tag=$(sed -n 's/^upstream_tag:[[:space:]]*//p' "$skill/references/compatibility.md")
if [ -n "$tag" ] && sh "$root/scripts/sync-upstream-skill.sh" --check "$tag"; then
	pass "vendored files equal upstream $tag"
else fail "vendored files equal upstream ${tag:-<no tag>}"; fi

# claude plugin validate, when Claude Code is installed.
if command -v claude >/dev/null 2>&1; then
	if claude plugin validate --strict "$plugin" >/dev/null && claude plugin validate --strict "$root" >/dev/null; then
		pass "claude plugin validate --strict passes"
	else fail "claude plugin validate --strict passes"; fi
else
	echo "skip claude plugin validate: claude is not installed"
fi

[ $failures -eq 0 ] || {
	echo "$failures structure test(s) failed"
	exit 1
}
echo "all structure tests passed"
