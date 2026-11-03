# Git operations (DP3)

Procedures use only the seven operations in this file. This file binds each
operation to the tools of the GitLab MCP server and the GitHub MCP server. A
procedure never calls a connector tool that this file does not name.

The bindings follow the GitLab and GitHub MCP documentation of November 2026.
If a tool rejects a parameter, read the schema that the connector reports for
the tool, use the parameter with the same meaning, and tell the person which
binding differed.

In the GitLab bindings, `project_id` is the full project path, for example
`acme/orders`. In the GitHub bindings, `owner` and `repo` are the two parts of
`acme/orders`.

## The operations

| Operation | What it does | GitLab MCP server | GitHub MCP server |
| --- | --- | --- | --- |
| resolve-ref | Gets the commit SHA of a branch, and the name of the default branch | `get_commit` | `get_commit` |
| list-model | Lists the files of `model_path` at a commit | `list_repository_tree` | `get_repository_tree` |
| read-file | Reads one file at a commit | `get_repository_file` | `get_file_contents` |
| commit-branch | Makes a new branch with all changed files in one commit | `add_commit` | `create_branch`, then `push_files` |
| open-mr | Opens an MR, as a Draft when the procedure asks | `save_merge_request` | `create_pull_request` |
| read-mr | Gets the base commit, the head commit, and the changed files of an MR | `get_merge_request` | `pull_request_read` |
| comment-mr | Adds one comment to an MR | `save_note` | `add_issue_comment` |

## Bindings

### resolve-ref

GitLab:

- Without a branch name, call `get_project` with `project_id` and read
  `default_branch`.
- Call `get_commit` with `project_id` and `commit_sha` set to the branch name.
  Read the full commit SHA from the result.

GitHub:

- Without a branch name, call `get_commit` with `sha` set to `HEAD`. To find
  the name of the default branch, call `search_repositories` with the query
  `repo:<owner>/<repo>` and read `default_branch`.
- Call `get_commit` with `owner`, `repo`, `sha` set to the branch name, and
  `detail` set to `none`. Read the full commit SHA from the result.

### list-model

GitLab: call `list_repository_tree` with `project_id`, `path` set to
`model_path`, `ref` set to the commit SHA, and `recursive` set to false. When
`pageInfo.hasNextPage` is true, call again with `after` set to
`pageInfo.endCursor`.

GitHub: call `get_repository_tree` with `owner`, `repo`, `tree_sha` set to the
commit SHA, `path_filter` set to `model_path` followed by `/`, and `recursive`
set to true. Keep only the entries directly in `model_path`.

Keep only entries of type file (GitLab `blob`, GitHub `blob` or `file`) whose
names end in `.em.hcl`.

### read-file

GitLab: call `get_repository_file` with `project_id`, `file_path`, and `ref`
set to the commit SHA. The tool returns at most 2000 lines. When
`metadata.truncated` is true, call again with the `offset` that
`system_instruction` names, until you have all lines. Compare the size of the
written file with `metadata.size_bytes`.

GitHub: call `get_file_contents` with `owner`, `repo`, `path`, and `sha` set to
the commit SHA. Decode base64 content. Compare the size of the written file
with the `size` of the result.

### commit-branch

Input: the snapshot commit S, a new branch name, a commit message, and the
list of changed files. Each changed file is created, updated, or deleted.

The branch name is `branch_prefix`, then a short name of the change in lower
case with `-` between words, then `-`, then the first 8 characters of S. For
example: `model/add-cancel-appointment-1a2b3c4d`.

GitLab: call `add_commit` once with `project_id`, `branch` set to the new
name, `start_sha` set to S, `commit_message`, and `actions`. Each action has
`action` (`create`, `update`, or `delete`), `file_path`, and for `create` and
`update` the full file `content`. Never use `old_str` and `new_str`, because
the branch must hold exactly the files that you validated. `start_sha` needs
GitLab 19.4 or later.

GitHub: the connector cannot start a branch at a commit. So:

1. Run resolve-ref on the default branch again. If its SHA is not S, the
   default branch moved after the snapshot. Go back to step E1 of em-change
   one time with the new SHA. If it moved again, stop and report.
2. Call `create_branch` with `owner`, `repo`, `branch` set to the new name,
   and `from_branch` set to the default branch.
3. Call `push_files` with `owner`, `repo`, `branch` set to the new name,
   `message`, and `files`. Each file has `path` and the full `content` of a
   created or updated file.
4. For each deleted file, call `delete_file` with `owner`, `repo`, `path`,
   `branch` set to the new name, and `message`. This adds one commit for each
   deleted file.

Never commit to a branch that this procedure did not make in this run.

### open-mr

Input: the new branch, the target branch, a title, a description, and Draft
or ready.

GitLab: call `save_merge_request` with `project_id`, `source_branch`,
`target_branch`, `title`, `description`, and `labels` set to `mr_labels`. For
a Draft, start the title with `Draft: `. Do not pass `merge_request_iid`,
because that updates an existing MR.

GitHub: call `create_pull_request` with `owner`, `repo`, `head` set to the new
branch, `base` set to the target branch, `title`, `body`, and `draft` set to
true for a Draft.

### read-mr

Input: an MR number or URL.

GitLab: call `get_merge_request` with `url`, or with `project_id` and
`merge_request_iid`. Read `source_branch`, `target_branch`,
`diff_refs.base_sha`, `diff_refs.head_sha`, and `web_url`. Then call
`get_merge_request` again with `include` set to `["diffs"]` and read the paths
of the changed files. On GitLab before 19.5, `get_merge_request_diffs` gives
the same paths.

GitHub: call `pull_request_read` with `method` set to `get`, `owner`, `repo`,
and `pullNumber`. Read `head.ref`, `base.ref`, `base.sha`, `head.sha`, and
`html_url`. Then call it with `method` set to `get_files` for the paths of the
changed files.

The base commit is the commit where the MR branch starts on the target branch.
The head commit is the last commit of the MR branch.

### comment-mr

Input: an MR and the comment text. Before the call, check each line of the
text. If a line starts with `/`, rewrite it so that it starts with a word.

GitLab: call `save_note` with `project_id`, `merge_request_iid`, and `body`.

GitHub: call `add_issue_comment` with `owner`, `repo`, `issue_number` set to
the pull request number, and `body`.

## Rules for every binding

- commit-branch starts the new branch at the snapshot commit, so the branch
  holds exactly the files that Claude validated.
- No procedure calls `accept_merge_request`, `merge_pull_request`,
  `save_merge_request_review`, `create_or_update_file`, or a tool that writes
  to the default branch.
- A comment or description line never starts with `/`.
- If a tool is missing, stop. Name the missing tool, and suggest em-setup.
