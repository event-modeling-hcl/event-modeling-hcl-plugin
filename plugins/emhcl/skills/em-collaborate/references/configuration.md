# Configuration: `.emhcl.yml`

Each model repository has one `.emhcl.yml` file at its root. All rules that
are specific to a team live there, so the plugin stays generic.

Each key has exactly one owner. Only the owner decides what the key does. Other
parts only read it. The keys are flat `key: value` lines, so a shell script can
read a key with one `sed` command.

```yaml
# The owner of each key is in brackets. Other parts only read the key.
emhcl_version: 0.16.0            # [DP1] emhcl release for Claude and CI
model_path: model                # [DP3] one folder; emhcl reads only the .em.hcl files directly in it
branch_prefix: model/            # [DP3] prefix of each new branch
mr_labels: [event-model]         # [DP3] labels on each new MR
reviewers_hint: "slice owner from CODEOWNERS"   # [DP3] text for the MR description
merge_profile: strict            # [DP5] CI gate; em-change opens a Draft MR when the model fails it
draft_profile: workshop          # [commands] default profile for em-view and em-validate
canonical_url: ""                # [DP5] GitLab Pages URL of the default branch
team_artifact_url: ""            # [DP4] shared artifact that mirrors the default branch
```

## Keys

| Key | Owner | Meaning | Value when absent |
| --- | --- | --- | --- |
| `emhcl_version` | DP1, `install-emhcl.sh` | The emhcl release that Claude and CI install. Only `install-emhcl.sh` reads it. | None. The installer stops. |
| `model_path` | DP3, Git port | The folder of the model, relative to the repository root. emhcl reads only the `.em.hcl` files directly in it. | `model` |
| `branch_prefix` | DP3, Git port | The start of the name of each branch that em-change or em-setup makes. | `model/` |
| `mr_labels` | DP3, Git port | Labels on each new MR. GitHub pull requests get no labels from the plugin. | `[]` |
| `reviewers_hint` | DP3, Git port | Text in the MR description that tells the author whom to ask for review. The plugin does not assign reviewers. | `""` |
| `merge_profile` | DP5, CI templates | The profile of the CI job `emhcl-validate`. em-change opens a Draft MR when the model fails it, and em-review validates with it. | `strict` |
| `draft_profile` | Commands | The profile of em-view and em-validate when the person names none. | `workshop` |
| `canonical_url` | DP5, CI templates | The URL where the CI job `pages` publishes the default branch. em-sync and em-view name it as the canonical view. | `""` |
| `team_artifact_url` | DP4, diagram publisher | The shared artifact that mirrors the default branch. em-sync republishes to it. | `""` |

The profiles are `workshop`, `valid`, and `strict`. Core errors are errors in
each profile. The profile sets only the severity of the judgment codes
`EM401` to `EM406`. `strict` makes `EM404` and `EM406` errors.

## Read the file

Read each key from its line `key: value`. Remove a trailing comment that
starts with ` #`. Remove the quotes around a string. A list such as
`[event-model, model]` holds names separated by commas. Report a key that this
table does not name, and then ignore it.

## Missing configuration

A repository without `.emhcl.yml` has no pin, so neither Claude nor CI can
know which emhcl to use.

- em-setup proposes the file through an MR. See its procedure.
- em-view and em-validate can still run. Write a temporary `.emhcl.yml` in
  the snapshot folder with the values of the table above, and with
  `emhcl_version` set to `emhcl_max_tested` from
  [compatibility.md](compatibility.md). Say in the report that the repository
  has no `.emhcl.yml`, and suggest em-setup.
- em-change, em-review, and em-sync stop and suggest em-setup. A proposal or a
  review needs the same pin that CI uses.

## A proposed file

em-setup proposes this file. Set `emhcl_version` to `emhcl_max_tested` from
[compatibility.md](compatibility.md). Set `model_path` to the folder that holds
the `.em.hcl` files. If several folders hold `.em.hcl` files, ask the person
which folder is the model. Keep the comments, because they name the owners.
