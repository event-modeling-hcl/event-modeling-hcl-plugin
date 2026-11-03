#!/bin/sh
# install-emhcl.sh installs the emhcl release that .emhcl.yml pins.
#
# This script is DP1 of the emhcl plugin. Claude and CI both run it, so both
# get the same validator for each commit. It is the only reader of the key
# emhcl_version.
#
# Usage: install-emhcl.sh [--config <path to .emhcl.yml>] [--bin-dir <folder>]
#
# The script downloads emhcl_<version>_<os>_<arch>.tar.gz (.zip on Windows) and
# checksums.txt from the GitHub release, and installs the binary only when the
# SHA-256 sums match. When the download fails, it runs go install at the same
# tag. A wrong sum stops the script; it never falls back after a wrong sum.
#
# Output: the absolute path of the installed binary, as the last line on
# stdout. Messages go to stderr.
#
# Environment:
#   EMHCL_BIN_DIR      install folder when --bin-dir is absent ($HOME/.local/bin)
#   EMHCL_RELEASE_URL  base URL of the release downloads (tests use a file:// URL)
#   EMHCL_NO_GO        set to 1 to turn off the go install fallback
#
# Exit status: 0 installed, 1 failure, 2 usage error.
set -eu

config=.emhcl.yml
bin_dir=${EMHCL_BIN_DIR:-"${HOME:-.}/.local/bin"}
release_url=${EMHCL_RELEASE_URL:-https://github.com/event-modeling-hcl/eventmodeling-hcl/releases/download}
module=github.com/event-modeling-hcl/eventmodeling-hcl/cmd/emhcl

say() { printf 'install-emhcl: %s\n' "$*" >&2; }
fail() { say "$*"; exit 1; }
usage() {
	say "usage: install-emhcl.sh [--config <path to .emhcl.yml>] [--bin-dir <folder>]"
	exit 2
}

while [ $# -gt 0 ]; do
	case $1 in
	--config)
		[ $# -ge 2 ] || usage
		config=$2
		shift 2
		;;
	--bin-dir)
		[ $# -ge 2 ] || usage
		bin_dir=$2
		shift 2
		;;
	*) usage ;;
	esac
done

[ -f "$config" ] || fail "$config does not exist"

# The keys of .emhcl.yml are flat, so one sed command reads the pin. Quotes and
# a leading v are optional: 0.16.0, "0.16.0", and v0.16.0 are the same pin.
version=$(sed -n \
	"s/^emhcl_version:[[:space:]]*[\"']\{0,1\}v\{0,1\}\([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\(-[0-9A-Za-z.]*\)\{0,1\}\)[\"']\{0,1\}[[:space:]]*\(#.*\)\{0,1\}$/\1/p" \
	"$config" | head -n 1)
[ -n "$version" ] || fail "$config has no emhcl_version like 0.16.0"
tag=v$version

case $(uname -s) in
Linux) os=linux ;;
Darwin) os=darwin ;;
MINGW* | MSYS* | CYGWIN*) os=windows ;;
*) os="" ;;
esac
case $(uname -m) in
x86_64 | amd64) arch=amd64 ;;
aarch64 | arm64) arch=arm64 ;;
*) arch="" ;;
esac
exe=emhcl
ext=tar.gz
if [ "$os" = windows ]; then
	exe=emhcl.exe
	ext=zip
fi

mkdir -p "$bin_dir"
bin_dir=$(cd "$bin_dir" && pwd)
target=$bin_dir/$exe

# reports_tag BINARY succeeds when "BINARY version" names the pinned tag.
reports_tag() {
	out=$("$1" version 2>/dev/null) || return 1
	case " $out " in
	*[[:space:]]"$tag"[[:space:]]*) return 0 ;;
	*) return 1 ;;
	esac
}

if [ -x "$target" ] && reports_tag "$target"; then
	say "emhcl $tag is already installed"
	printf '%s\n' "$target"
	exit 0
fi

fetch() {
	if command -v curl >/dev/null 2>&1; then
		curl -fsSL --retry 2 -o "$2" "$1"
	elif command -v wget >/dev/null 2>&1; then
		wget -q -O "$2" "$1"
	else
		say "neither curl nor wget is available"
		return 1
	fi
}

sha256() {
	if command -v sha256sum >/dev/null 2>&1; then
		sha256sum "$1" | cut -d ' ' -f 1
	elif command -v shasum >/dev/null 2>&1; then
		shasum -a 256 "$1" | cut -d ' ' -f 1
	else
		fail "neither sha256sum nor shasum is available, so the download cannot be checked"
	fi
}

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT INT TERM

method=""
archive=emhcl_${version}_${os}_${arch}.$ext
if [ -z "$os" ] || [ -z "$arch" ]; then
	say "no release archive for $(uname -s) $(uname -m)"
elif fetch "$release_url/$tag/$archive" "$tmp/$archive" &&
	fetch "$release_url/$tag/checksums.txt" "$tmp/checksums.txt"; then
	expected=$(awk -v f="$archive" '$2 == f || $2 == "*" f { print $1; exit }' "$tmp/checksums.txt")
	[ -n "$expected" ] || fail "checksums.txt of $tag has no line for $archive. Nothing was installed."
	actual=$(sha256 "$tmp/$archive")
	[ "$actual" = "$expected" ] ||
		fail "SHA-256 of $archive is $actual, but checksums.txt says $expected. Nothing was installed."
	mkdir "$tmp/x"
	if [ "$ext" = zip ]; then
		unzip -q "$tmp/$archive" -d "$tmp/x"
	else
		tar -xzf "$tmp/$archive" -C "$tmp/x"
	fi
	[ -f "$tmp/x/$exe" ] || fail "$archive has no $exe. Nothing was installed."
	cp "$tmp/x/$exe" "$target.new"
	chmod 755 "$target.new"
	mv -f "$target.new" "$target"
	method="release archive $archive"
else
	say "download of $archive from $release_url/$tag failed"
fi

if [ -z "$method" ]; then
	if [ "${EMHCL_NO_GO:-0}" = 1 ]; then
		fail "go install fallback is off (EMHCL_NO_GO=1). Nothing was installed."
	fi
	command -v go >/dev/null 2>&1 || fail "go is not available for the fallback. Nothing was installed."
	say "falling back to go install $module@$tag"
	GOBIN=$bin_dir go install "$module@$tag" || fail "go install $module@$tag failed"
	method="go install $module@$tag"
fi

reports_tag "$target" || fail "$target does not report $tag after the install"
say "installed emhcl $tag from $method"
printf '%s\n' "$target"
