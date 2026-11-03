#!/bin/sh
# Tests of install-emhcl.sh (DP1) against a fake release on a file:// URL.
# No network. Run from any folder: sh tests/install-emhcl.test.sh
set -u

root=$(cd "$(dirname "$0")/.." && pwd)
script=$root/plugins/emhcl/skills/em-collaborate/scripts/install-emhcl.sh
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT INT TERM

case $(uname -s) in Linux) os=linux ;; Darwin) os=darwin ;; *) echo "skip: tests need Linux or macOS" && exit 0 ;; esac
case $(uname -m) in x86_64 | amd64) arch=amd64 ;; aarch64 | arm64) arch=arm64 ;; *) echo "skip: unknown CPU" && exit 0 ;; esac

sha256() {
	if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d ' ' -f 1; else shasum -a 256 "$1" | cut -d ' ' -f 1; fi
}

# make_release VERSION [WRONG_SUM] writes a fake release of VERSION under $work/releases.
make_release() {
	dir=$work/releases/v$1
	mkdir -p "$dir" "$work/build"
	printf '#!/bin/sh\necho "emhcl v%s"\n' "$1" >"$work/build/emhcl"
	chmod 755 "$work/build/emhcl"
	archive=emhcl_$1_${os}_${arch}.tar.gz
	tar -czf "$dir/$archive" -C "$work/build" emhcl
	sum=$(sha256 "$dir/$archive")
	if [ "${2:-}" = wrong ]; then sum=0000000000000000000000000000000000000000000000000000000000000000; fi
	printf '%s  %s\n' "$sum" "$archive" >"$dir/checksums.txt"
}

failures=0
pass() { printf 'ok   %s\n' "$1"; }
fail() {
	printf 'FAIL %s\n' "$1"
	failures=$((failures + 1))
}

# run CONFIG_TEXT BIN_DIR: runs the script and sets $status and $out (last stdout line).
run() {
	printf '%s\n' "$1" >"$work/.emhcl.yml"
	out=$(EMHCL_RELEASE_URL=file://$work/releases EMHCL_NO_GO=1 sh "$script" --config "$work/.emhcl.yml" --bin-dir "$2" 2>"$work/stderr")
	status=$?
	out=$(printf '%s\n' "$out" | tail -n 1)
}

make_release 9.9.8
make_release 9.9.9
make_release 9.9.7 wrong

run 'emhcl_version: 9.9.9 # [DP1] pin' "$work/bin"
if [ $status -eq 0 ] && [ "$out" = "$work/bin/emhcl" ] && [ "$("$work/bin/emhcl" version)" = "emhcl v9.9.9" ]; then
	pass "a correct sum installs the pinned release and prints its path"
else fail "a correct sum installs the pinned release (status $status, out $out)"; fi

run 'emhcl_version: "v9.9.8"' "$work/bin"
if [ $status -eq 0 ] && [ "$("$work/bin/emhcl" version)" = "emhcl v9.9.8" ]; then
	pass "a change of the pin changes the installed release"
else fail "a change of the pin changes the installed release (status $status)"; fi

run 'emhcl_version: 9.9.7' "$work/bin"
if [ $status -eq 1 ] && [ "$("$work/bin/emhcl" version)" = "emhcl v9.9.8" ] && grep -q 'SHA-256' "$work/stderr"; then
	pass "a wrong sum stops the install and keeps the old binary"
else fail "a wrong sum stops the install (status $status)"; fi

run 'emhcl_version: 9.9.7' "$work/fresh"
if [ $status -eq 1 ] && [ ! -e "$work/fresh/emhcl" ]; then
	pass "a wrong sum installs nothing in an empty folder"
else fail "a wrong sum installs nothing in an empty folder (status $status)"; fi

run 'emhcl_version: 9.9.6' "$work/bin"
if [ $status -eq 1 ] && grep -q 'download' "$work/stderr"; then
	pass "a missing release fails when the go fallback is off"
else fail "a missing release fails when the go fallback is off (status $status)"; fi

run 'model_path: model' "$work/bin"
if [ $status -eq 1 ] && grep -q 'no emhcl_version' "$work/stderr"; then
	pass "a configuration without a pin fails"
else fail "a configuration without a pin fails (status $status)"; fi

sh "$script" --bin-dir >/dev/null 2>&1
if [ $? -eq 2 ]; then pass "a usage error exits 2"; else fail "a usage error exits 2"; fi

[ $failures -eq 0 ] || {
	echo "$failures test(s) failed"
	exit 1
}
echo "all install-emhcl tests passed"
