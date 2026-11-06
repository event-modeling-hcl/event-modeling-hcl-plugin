---
type: llm
---

Judge the actual agent behavior, final answer, tool calls, and resulting files. Do not grade source text or demand specific skill names.

PASS only if all conditions hold:
1. Every block moves whole into a file directly in `clinic/`. No block spans two files, and no `include` or `import` block is invented.
2. The bounded context with all its events, aggregates, and field types is in one file.
3. The single `board` block moves whole into one file and keeps its workflow list unchanged, so the story order is the same. The chapter keeps its membership; no workflow is in two chapters.
4. File names can use a prefix for human reading order, but the reply does not rely on file order for the board. No ID is declared twice across files.
5. With emhcl v0.17.0 or newer, the folder is formatted with `emhcl fmt -w clinic` or by formatting each member file, and validated with `emhcl validate clinic`. The agent does not falsely claim current fmt refuses folders, validate members separately as complete models, or claim an older CLI verifies v0.7.0.
6. The owner_notice_timing hotspot stays open and attached to processor.notify_owner.owner_notifier, with its original question. No timing rule is invented, the reply does not call the model implementation-ready, and any strict EM406 failure is reported rather than suppressed.

FAIL if any condition is missing. Tool availability limits must be stated honestly.
