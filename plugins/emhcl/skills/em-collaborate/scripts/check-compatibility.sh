#!/bin/sh
# check-compatibility.sh compares an installed emhcl with the range that the
# skill event-modeling-hcl supports (the FR2 and DP1 cell of the design matrix).
#
# Usage: check-compatibility.sh <path to the emhcl binary>
#
# The script asks the binary for its version, so it never reads .emhcl.yml.
# It reads emhcl_min and emhcl_max_tested from references/compatibility.md.
#
# Exit status:
#   0  the version is inside the supported range
#   1  the version is older than emhcl_min, or unknown: stop
#   3  the version is newer than emhcl_max_tested: warn and continue
#   2  usage error
set -eu

[ $# -eq 1 ] || {
	echo "usage: check-compatibility.sh <path to the emhcl binary>" >&2
	exit 2
}
compat=$(cd "$(dirname "$0")/.." && pwd)/references/compatibility.md

key() { sed -n "s/^$1:[[:space:]]*v\{0,1\}\([0-9][0-9.]*\).*$/\1/p" "$compat" | head -n 1; }
min=$(key emhcl_min)
max=$(key emhcl_max_tested)
[ -n "$min" ] && [ -n "$max" ] || {
	echo "check-compatibility: $compat has no emhcl_min or emhcl_max_tested" >&2
	exit 1
}

out=$("$1" version 2>/dev/null) || {
	echo "check-compatibility: $1 version failed" >&2
	exit 1
}
version=$(printf '%s\n' "$out" | sed -n 's/.*[[:space:]]v\([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\).*/\1/p' | head -n 1)
[ -n "$version" ] || {
	echo "check-compatibility: '$out' names no release version, so the range cannot be checked" >&2
	exit 1
}

# cmp_version A B prints -1, 0, or 1 for major.minor.patch versions.
cmp_version() {
	echo "$1 $2" | awk '{
		split($1, a, "."); split($2, b, ".")
		for (i = 1; i <= 3; i++) {
			if (a[i] + 0 < b[i] + 0) { print -1; exit }
			if (a[i] + 0 > b[i] + 0) { print 1; exit }
		}
		print 0
	}'
}

if [ "$(cmp_version "$version" "$min")" = -1 ]; then
	echo "check-compatibility: emhcl $version is older than $min, the oldest release that the skill supports. Pin $min or newer in .emhcl.yml." >&2
	exit 1
fi
if [ "$(cmp_version "$version" "$max")" = 1 ]; then
	echo "check-compatibility: emhcl $version is newer than $max, the newest release tested with this plugin. Results can differ; update the plugin." >&2
	exit 3
fi
echo "check-compatibility: emhcl $version is inside the supported range $min to $max"
