#!/bin/sh
# Structure tests of the plugin repository. They keep the zeros of the design
# matrix true. Run from any folder: sh tests/structure.sh
# The example check downloads the upstream tag (or uses UPSTREAM_REPO).
set -u

root=$(cd "$(dirname "$0")/.." && pwd)
plugin=$root/plugins/emhcl
skills_plugin=$root/plugins/emhcl-skills
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
for f in "$plugin"/skills/*/SKILL.md "$plugin"/commands/*.md "$skills_plugin"/skills/*/SKILL.md; do
	if [ "$(head -n 1 "$f")" = --- ] && sed -n '2,/^---$/p' "$f" | grep -q '^description:[[:space:]]*[^[:space:]]'; then
		:
	else fail "front matter with a description: ${f#"$root"/}"; fi
done
pass "front matter checked for each skill and command"

# FR1 and DP5: no CI template names an emhcl version.
# Plugin release tags in usage comments are not emhcl CLI versions.
templates="$root/ci-templates/emhcl.gitlab-ci.yml $root/.github/workflows/emhcl-model.yml"
if grep -nE 'emhcl_version|[0-9]+\.[0-9]+\.[0-9]+|eventmodeling-hcl/releases|cmd/emhcl@' $templates | grep -vE 'event-modeling-hcl-plugin/(\.github/workflows/emhcl-model\.yml@)?v[0-9]+\.[0-9]+\.[0-9]+(/ci-templates/emhcl\.gitlab-ci\.yml|$)|plugin_ref: v[0-9]+\.[0-9]+\.[0-9]+$'; then
	fail "a CI template names an emhcl version"
else pass "no CI template names an emhcl version"; fi

# DP1: only install-emhcl.sh reads emhcl_version. Other code only writes or documents it.
readers=$(grep -rlE 'sed[^|]*emhcl_version' "$root" --include='*.sh' --include='*.yml' | grep -v -e '/install-emhcl.sh$' -e '/sync-upstream.sh$' -e '/tests/')
[ -z "$readers" ] && pass "only install-emhcl.sh reads emhcl_version" || fail "other readers of emhcl_version: $readers"

# Each key of an example configuration carries one owner tag.
for cfg in "$root/examples/pet-clinic/.emhcl.yml"; do
	bad=$(grep -vE '^#|^$' "$cfg" | grep -vE '# \[(DP1|DP3|DP4|DP5|commands)\]' || true)
	[ -z "$bad" ] && pass "each key of $(basename "$(dirname "$cfg")")/.emhcl.yml has one owner" || fail "keys without an owner: $bad"
done

# The marketplace entries and the manifests agree on the plugin names.
if grep -q '"name": "event-modeling-hcl-plugin"' "$root/.claude-plugin/marketplace.json" && grep -q '"name": "event-modeling-hcl-plugin"' "$plugin/.claude-plugin/plugin.json" &&
	grep -q '"name": "event-modeling-skills"' "$root/.claude-plugin/marketplace.json" && grep -q '"name": "event-modeling-skills"' "$skills_plugin/.claude-plugin/plugin.json"; then
	pass "marketplace entries and manifest names agree"
else fail "marketplace entries and manifest names agree"; fi

# DP2: the main plugin reaches the language skill only through its dependency on event-modeling-skills.
if grep -q '"dependencies": \["event-modeling-skills"\]' "$plugin/.claude-plugin/plugin.json" &&
	[ -f "$skills_plugin/skills/event-modeling-hcl/SKILL.md" ] && [ ! -e "$plugin/skills/event-modeling-hcl" ]; then
	pass "event-modeling-hcl-plugin depends on event-modeling-skills for event-modeling-hcl"
else fail "event-modeling-hcl-plugin depends on event-modeling-skills for event-modeling-hcl"; fi

# DP0: the contract copies in the method skills equal contract/.
if sh "$root/scripts/build-contract.sh" --check >/dev/null; then
	pass "contract copies equal contract/"
else fail "contract copies equal contract/ (run scripts/build-contract.sh)"; fi

# A method skill never names another method skill. The language skill is a
# shared authority, not another model-part writer.
all_skills=$(cd "$skills_plugin/skills" && ls)
method_count=0
for dir in "$skills_plugin"/skills/eventmodeling-*/; do
	own=$(basename "$dir")
	method_count=$((method_count + 1))
	for other in $all_skills; do
		[ "$other" = "$own" ] && continue
		[ "$other" = event-modeling-hcl ] && continue
		hits=$(grep -rlE "(^|[^a-z-])$other([^a-z-]|$)" "$dir" || true)
		[ -z "$hits" ] || fail "$own names the skill $other in: $hits"
	done
	for kind in fires near-miss accepts; do
		[ -f "$skills_plugin/evals/${own#eventmodeling-}-$kind/prompt.md" ] || fail "$own has no eval ${own#eventmodeling-}-$kind"
	done
done
[ "$method_count" -eq 32 ] && pass "32 method skills, no peer names, each has three evals" || fail "expected 32 method skills, found $method_count"

# The procedures never name a merge tool except to forbid it.
if grep -rn 'accept_merge_request\|merge_pull_request' "$skill/references/procedures"; then
	fail "a procedure names a merge tool"
else pass "no procedure names a merge tool"; fi

# The example model and compatibility.md equal the upstream tag and the skill.
tag=$(sed -n 's/^upstream_tag:[[:space:]]*//p' "$skill/references/compatibility.md")
if [ -n "$tag" ] && sh "$root/scripts/sync-upstream.sh" --check "$tag"; then
	pass "example and compatibility equal upstream $tag"
else fail "example and compatibility equal upstream ${tag:-<no tag>}"; fi

# claude plugin validate, when Claude Code is installed.
if command -v claude >/dev/null 2>&1; then
	if claude plugin validate --strict "$plugin" >/dev/null && claude plugin validate --strict "$skills_plugin" >/dev/null &&
		claude plugin validate --strict "$root" >/dev/null; then
		pass "claude plugin validate --strict passes"
	else fail "claude plugin validate --strict passes"; fi
	# A nonmatching case filter loads every prompt and grader without model calls.
	for eval_plugin in "$plugin" "$skills_plugin"; do
		loader_status=0
		loader=$(claude plugin eval "$eval_plugin" --trust-plugin --case __loader_only__ --no-publish 2>&1) || loader_status=$?
		if [ "$loader_status" -eq 1 ] &&
			printf '%s\n' "$loader" | grep -q '^No eval cases found matching --case "__loader_only__"' &&
			! printf '%s\n' "$loader" | grep -qE 'invalid YAML|failed to load|^✗'; then
			pass "eval loader parses every case in $(basename "$eval_plugin")"
		else
			printf '%s\n' "$loader"
			fail "eval loader parses every case in $(basename "$eval_plugin")"
		fi
	done
else
	echo "skip claude plugin validate: claude is not installed"
fi

[ $failures -eq 0 ] || {
	echo "$failures structure test(s) failed"
	exit 1
}
echo "all structure tests passed"
