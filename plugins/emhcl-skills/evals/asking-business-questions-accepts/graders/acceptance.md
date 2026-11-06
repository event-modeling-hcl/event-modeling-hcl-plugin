---
type: llm
---
PASS if every question in the reply points at something unclear or missing in the given model and names the element it is about, with a reason that the model shows (for example the return step has no refusal case, or nobody is told what happens after the 3-rental limit), AND no question text uses the words event, command, read model, slice, actor, scenario, given, when, then, or a shape name such as bed, chair, or shelf. FAIL if a question asks about something the model already answers (for example the open-rental limit itself), invents a requirement with no basis in the model, or uses one of the banned model words in the question text.
