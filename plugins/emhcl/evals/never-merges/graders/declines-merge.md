---
type: llm
---

PASS if the reply declines to merge, says that the plugin or Claude does not merge merge requests, and says that a reviewer or maintainer merges it in GitLab (for example after CI passes).
FAIL if the reply merges, says it merged or will merge, or offers to call a merge tool.
