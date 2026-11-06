#!/bin/sh
# check-source-overlap.sh reports each run of eight or more words that the
# method contract or a method skill shares with a source skill of unknown
# license (contract/CREDITS.md).
#
# Usage: scripts/check-source-overlap.sh [source folder]   default tmp/_to_use
#
# Exit status: 0 no shared run, 1 a shared run exists, 2 the source folder
# does not exist.
set -eu

root=$(cd "$(dirname "$0")/.." && pwd)
src=${1:-$root/tmp/_to_use}
[ -d "$src" ] || {
	echo "check-source-overlap: no source folder $src" >&2
	exit 2
}

targets=$( (ls "$root/contract/method.md" "$root/contract/hcl-binding.md"
	find "$root/plugins/emhcl-skills/skills" -path '*/eventmodeling-*' -name '*.md' ! -name contract.md
	find "$root/plugins/emhcl-skills/evals" -name '*.md') | sort)
sources=$(find "$src" -name '*.md' | sort)

# Words are runs of lowercase letters, digits, and apostrophes.
# shellcheck disable=SC2086
awk -v n=8 '
	function words(line,   s) {
		s = tolower(line)
		gsub(/[^a-z0-9'"'"']+/, " ", s)
		return s
	}
	FNR == 1 { fileno++; if (fileno <= nsrc) { sl = 0; delete srcbuf } else { cnt = 0; delete win; last = -1 } }
	{
		k = split(words($0), w, " ")
		for (i = 1; i <= k; i++) {
			if (w[i] == "") continue
			if (fileno <= nsrc) {
				srcbuf[++sl] = w[i]
				if (sl >= n) { g = srcbuf[sl - n + 1]; for (j = sl - n + 2; j <= sl; j++) g = g " " srcbuf[j]; seen[g] = 1 }
			} else {
				win[++cnt] = w[i]
				if (cnt >= n) {
					g = win[cnt - n + 1]; for (j = cnt - n + 2; j <= cnt; j++) g = g " " win[j]
					if (g in seen) {
						if (last != cnt - 1) { print FILENAME ": " g; hits++ }
						last = cnt
					}
				}
			}
		}
	}
	END { if (hits) { print hits " shared run(s)"; exit 1 } print "no shared run of " n " words" }
' nsrc="$(echo "$sources" | wc -l)" $sources $targets
