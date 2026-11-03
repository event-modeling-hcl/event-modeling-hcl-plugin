# Compatibility

The script `scripts/sync-upstream-skill.sh` writes this file when it copies
the upstream skill. Do not edit it by hand.

The vendored skill `event-modeling-hcl` comes from the upstream tag below. It
supports each emhcl release from `emhcl_min` on. The plugin release was tested
with `emhcl_max_tested`. The script `check-compatibility.sh` reads these keys.

```text
upstream_tag: v0.16.0
skill_version: 2.5.0
spec_version: v0.7.0
emhcl_min: 0.16.0
emhcl_max_tested: 0.16.0
```
