# Diagrams (DP4)

The diagram publisher turns a snapshot folder into an artifact. It receives a
folder, a title, and an optional artifact URL from the procedure. It never
calls Git tools, and it never changes the model files.

There are three views of the model:

| View | Made by | Shows | Who reads it |
| --- | --- | --- | --- |
| GitLab Pages (or GitHub Pages) | CI job `pages` after each merge | The default branch | Everyone. This is the canonical view, at `canonical_url`. |
| Team artifact | em-sync | The default branch | The team, inside Claude. Teammates comment on slices there. |
| Proposal artifact | em-change, em-review, em-view | One branch or one MR | The author and the reviewers |

## Render

```sh
"$EMHCL" diagram --title "<title>" -o <work>/<name>.html <snapshot folder>/<model_path>
```

The title names the repository, the branch, and the first 8 characters of the
commit SHA:

| Procedure | Title |
| --- | --- |
| em-view, em-sync | `<project> <branch> @ <short SHA>` |
| em-review | `<project> <source branch> @ <short head SHA>` |
| em-change | `<project> <new branch> @ <short base SHA> (proposal)` |

The em-change title names the base commit, because the new commit does not
exist yet when the diagram is made.

`emhcl diagram` exits 0 and prints `wrote <file>`. It can also print
diagnostics. They do not stop the diagram.

## Publish

1. Check the size. If the file is larger than 16 MiB, do not publish. Say that
   the diagram is too large for an artifact, and name `canonical_url` if it is
   set.
2. Publish the HTML file itself as an artifact, with the same title. Never
   rewrite, restyle, shorten, or retype the HTML, and do not apply a design to
   it. The page is the output of emhcl, so it must stay the same as in CI.
3. With an artifact URL from the procedure, publish the file as a new version
   of that artifact. Without a URL, publish a new artifact.

If the surface cannot publish a file as an artifact, do not make a page by
hand. Give the person the HTML file instead, and report `Artifact: none` with
the reason. A procedure then says in the MR description or comment that no
diagram link exists.

## Share

A new artifact is private to its author. Claude cannot change who can see it.
After each new artifact, tell the person:

> Open the artifact, click Share, and give access to the people who need it.
> For the team artifact, select everyone at your organization.

To republish the team artifact, a person needs "Can edit" access. A person
with "Commenter" access can comment, but cannot republish.

## Comments on the team artifact

Teammates comment on slices in the team artifact. When a person asks Claude to
act on such a comment, read the comment, then run em-change with the request
in the comment. Never republish the team artifact from a branch other than the
default branch.
