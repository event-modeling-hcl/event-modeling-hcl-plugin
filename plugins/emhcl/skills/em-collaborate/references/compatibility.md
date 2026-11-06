# Compatibility

The script `scripts/sync-upstream.sh` writes this file. Do not edit it by
hand.

The skill `event-modeling-hcl` of the plugin `emhcl-skills` supports each
emhcl release from `emhcl_min` on. The plugin release was tested with
`emhcl_max_tested`, which is also the tag of the example model. The script
`check-compatibility.sh` reads these keys.

```text
upstream_tag: v0.17.0
skill_version: 3.1.0
spec_version: v0.8.0
emhcl_min: 0.17.0
emhcl_max_tested: 0.17.0
```
