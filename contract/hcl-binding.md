# HCL binding of the method contract

This file maps each part of the method contract to Event Modeling HCL v0.8.0. A method skill follows the sections of this file only when the model is an `.em.hcl` file or folder. The specification wins when this file and the specification differ. This file names no construct that the specification does not define.

## H0 Working on an `.em.hcl` model

1. The model is one `.em.hcl` file or one folder of `.em.hcl` files. Keep its shape. In a folder, IDs are global across the member files.
2. Write only the blocks and attributes that this binding names for your part. Never invent a block or an attribute. A method fact that HCL cannot hold stays out of the model. Report it to the person as a representation gap.
3. Use lower-snake-case labels that match `^[a-z][a-z0-9_]*$`. Write `title` only when the text differs from the label.
4. References are unquoted traversals, such as `event.rental.bike_rented`. Never quote a reference.
5. Each `field` and `subfield` needs an explicit `type`: a built-in type or a `field_type` traversal.
6. After each change, run `emhcl fmt -w <model>` and then `emhcl validate --profile workshop <model>`. Repair each core error (`EM000` to `EM305`) that your change caused. Stop after two failed repairs of one code on one element, and report the code, the location, and both attempts.
7. Copy tool output lines unchanged. Your own findings never carry an EM code.
8. Never change a workflow whose `status` is `review`, `done`, or `informational` unless the person asks for that change.

## H1 Roles

| Method fact | HCL |
| --- | --- |
| Human role | `actor "<id>" { auth_required = <true or false> }` |
| What a role can and cannot do | `description` of the `actor` |
| System actor inside the system | A `processor` in an `automation` workflow, named for its job |
| System actor outside the system | `system "<id>" { external = true }` and a `bounded_context` with `external = true` for its events |
| Team | `team "<id>" {}` |

`auth_required` is required. If no source states it, set the most likely value and write an assumption hotspot on the actor.

## H2 Events

| Method fact | HCL |
| --- | --- |
| Business event | `event "<id>"` inside the `bounded_context` that owns the fact |
| Identity and key facts | `field` blocks or a `fields` list of `field_type` traversals |
| Recurring domain concept | `field_type` inside the owning `bounded_context` |
| Event from another system | `event` inside a `bounded_context` with `external = true` |
| A value that the system fills | `generated = true` on the field |
| Personal data | `pii = true` on the field |

Name the event in past tense as a label, such as `bike_rented`.

## H3 Slices, chapters, and story order

A chapter and the board hold workflows, and a workflow is one slice: a `state_change` for one command, a `state_view` for one read model, or an `automation` for one processor. HCL has no place for a chapter of events or an order of events without workflows. Never create a workflow only to hold an event, a chapter, or a position in the story.

1. A workflow exists only for a slice that K3 identifies. The writer of the part that adds the first element of a slice creates its workflow: the screens writer for a screen action (`state_change`) or a screen that only shows data (`state_view`), the commands writer for a command without a screen, the automations writer for an automation, and the read models writer for a read model without a screen.
2. Until the slices exist, HCL has no place for the order of the story. The events, the stream identities, and the lifecycle states hold the facts that exist so far. A state records its path and whether it is an end, not its position. The order of the states appears only when the transitions exist, and the story order appears only when the board exists.
3. In an `.em.hcl` model, close the gates of K12 in this order: roles, events, streams, lifecycle states, screens, commands, lifecycle moves, automations, external mappings, read models, chapters, story order, command scenarios, read model scenarios, reviews, slice status, ownership, chapter summaries. A lifecycle move names a command, so the lifecycles gate closes in two steps: states before the commands, moves and refused moves after them.
4. The chapters writer writes `chapter "<id>" { workflows = [...] }` from the slices of each journey. A chapter needs at least one workflow (`EM005`). A workflow is in one chapter only (`EM014`). The chapter of an event follows from its workflows.
5. The story-order writer writes `board { workflows = [...] }` in business-time order. The board is the only story order. A workflow that is not on the board is not part of the story.
6. Triggers and preconditions of a step go into the `description` of its workflow, or into the lifecycle when they are states.
7. A workflow that a writer adds after the chapters and the board exist needs a place in both. Its creator writes a request with `concerns = "chapter"` and one with `concerns = "board"`.

## H4 Screens

| Method fact | HCL |
| --- | --- |
| Screen where a person acts | `screen` in the `state_change` workflow of its action. The screens writer creates that workflow, named for the action. |
| Screen where a person only looks | `screen` in a `state_view` workflow, created by the screens writer |
| The role of the screen | `actor = actor.<id>` |
| A request or response of a client program | `kind = "api"` and `api_endpoint` |
| A field that the person enters | `field` on the screen, with no `field_source` and no `generated`. The screen is its origin. `generated = true` means that the system fills the value, so it never marks input of a person. |
| A field that the screen shows | `field` on the screen, and a `field_source` from the read model when the read model exists |

A page with several actions is several screens. A screen that shows data waits for its read model. Write a request with `concerns = "readmodel"` for each read model that the screen needs and the model does not have.

## H5 Streams and lifecycles

| Method fact | HCL |
| --- | --- |
| Stream | `aggregate "<id>"` inside its `bounded_context` |
| Stream identity | `identity = field_type.<id>` on the `aggregate`. Each event of the aggregate then needs a field of that type (`EM018`). |
| Event of a stream | `aggregate = aggregate.<id>` on the `event` |
| Lifecycle | One top-level `lifecycle "<id>" { aggregate = aggregate.<context>.<id> }` for each aggregate |
| State | `state "<id>" { path = "main" }`, with `end = true` for an end state. `path` is `"main"`, `"cancel"`, `"failure"`, or `"compensation"`. |
| Move | `transition "<id>" { command = command.<workflow>.<id>, events = [...], before = [state.<id>], after = state.<id> }`. `before = []` starts the stream. |
| Refused move | `invalid_transition "<id>" { command = ..., before = [...], reason = "..." }` |

A lifecycle names commands. Write the states first. Write each move and each refused move when its command exists. Until then, the lifecycles gate stays open. One state and one command form a transition or an invalid transition, never both (`EM017`).

## H6 Commands

| Method fact | HCL |
| --- | --- |
| Command issued by a person | `command` in the `state_change` workflow of its screen, and `to = [command.<id>]` on the screen |
| Command issued by an automation | `command` in the `automation` workflow, and `to = [command.<id>]` on the processor |
| Success event | `to = [event.<context>.<id>]` on the command |
| Command fields | `field` blocks or a `fields` list. A context value (time, acting user, tenant) is a field with `generated = true`. |
| Precondition | An `invalid_transition` (H5) and a scenario with `error` (H9) |

Use `external_trigger = true` only when no issuer can be modeled. Never use `triggers` or `api_endpoint` as an issuer.

## H7 Automations and external mappings

| Method fact | HCL |
| --- | --- |
| Automation | `automation "<id>"` workflow with a `processor` |
| Todo list | A `readmodel` in the same workflow, with `question`. `from` lists the events that open and close items. `to = [processor.<id>]`. |
| Translation step | An `automation` whose todo list reads an event of an external `bounded_context`. There is no `translation` keyword. |
| Worker step | An `automation` whose todo list reads internal events only |
| Payload mapping | `field_source` blocks inside the translation workflow |
| Correlation key | `correlation_key = true` on the field |
| Duplicate key | `deduplication_key = true` on the field |

A todo list has no status field. Its `from` list includes the event that closes the work.

## H8 Read models and field origin

| Method fact | HCL |
| --- | --- |
| Read model | `readmodel "<id>"` in a `state_view` workflow, with the required `question` (the natural query) |
| Events that feed it | `from = [event.<context>.<id>, ...]` on the read model |
| Screen that shows it | `to = [screen.<id>]` on the read model |
| Same-name origin | The same field name or `field_type` on both sides of an edge |
| Renamed or derived origin | `field_source { inputs = [...], target = ... }` in the workflow of the target. `description` states the rule of a derived value. |
| Value that starts here | A value that a person enters starts on its screen with no marker. A value that the system fills where it starts (an identifier that the system makes when it records the fact, the current time, the acting user) gets `generated = true`. A value that a read model computes gets a `field_source` with its inputs and a `description` of the rule. `generated = true` is never a source link and never hides a gap. |
| Reason for wide fan-in | A `decision` (H10) on the read model field |

An event or command field has exactly one input (`EM202`). Each input reaches the target along one canonical edge of the workflow.

## H9 Scenarios

| Method fact | HCL |
| --- | --- |
| Command scenario | `scenario` in the `state_change` workflow: `given` events, one `when` command, `then` events or `error` |
| Case of a scenario | `case = "<value>"`: `happy_path`, `variant`, `refused_input`, `state_violation`, `business_duplicate`, `limit`, `authorization`, `alternative_path`, `external_failure`, `compensation` |
| Read model scenario | `scenario` in the `state_view` workflow: `given` events, no `when`, `then` read model |
| Read model case | `case = "appear"`, `"change"`, or `"disappear"` |
| A view before any event | `empty_history = true` and no `given` step |
| An intentionally empty list | `expect_empty_list = true` on the `then` step |
| An automation issues a command | An action form scenario: `when` the processor, `then` the command |
| An automation issues nothing | The same, with `expect_no_dispatch = true` on the `then` command step |
| Storyline | Several scenarios, or one scenario with ordered `given` steps. There is no `storyline` block. |
| Example values | `examples` on a step, or `example` on a field |
| A note | `comment { description = "..." }` inside the scenario |

Write `case` only when the business supports that case. A rejection is `then { error = "..." }` with the reason in domain words.

## H10 Records

| Method fact | HCL |
| --- | --- |
| Open question | `hotspot "<id>" { question = "...", on = <target> }` |
| Assumption | `hotspot` with `kind = "assumption"` |
| Request | `hotspot` with `kind = "request"` and `concerns` (`"event"`, `"aggregate"`, `"field_type"`, `"command"`, `"readmodel"`, `"screen"`, `"processor"`, `"scenario"`, `"workflow"`, `"board"`, `"chapter"`, `"actor"`, `"lifecycle"`, `"field_source"`) |
| Category and options | `category` (the eight K11 values) and `options` on the hotspot |
| Answered record | Write the answer as a `decision`. Reuse the hotspot's `on` target if that target is legal for a decision. For a whole-model hotspot, omit `on` from the decision. Set the hotspot's `status = "resolved"` and retain it. A `decision` cannot name a hotspot in `on` (`EM101`). |
| Decision | `decision "<id>" { statement = "...", reason = "...", on = <target> }`. Without `on`, it is about the whole model. |
| Accepted debt | `decision` with `kind = "accepted_debt"`. If a judgment signal exists, set `signal` to its exact code: `"EM401"`, `"EM402"`, `"EM403"`, `"EM404"`, `"EM405"`, or `"EM406"`. Otherwise omit `signal`. |
| Evidence source | `evidence_source "<id>" { kind = "document", location = "..." }`. `kind` is `"document"`, `"code"`, `"application"`, or `"person"`. |
| Evidence | `evidence "<id>" { certainty = "stated", source = evidence_source.<id>, location = "...", on = <target> }` |

A record `on` names one target: a catalog item, a workflow, an owner, an actor, a qualified element such as `command.rent_bike.rent_bike`, a lifecycle part, or a field reference. `"stated"` and `"implied"` evidence needs `source` (`EM000`). An open hotspot is an error in the `strict` profile (`EM406`).

## H11 Slices, ownership, and summaries

| Method fact | HCL |
| --- | --- |
| Slice | One workflow. A `state_change` holds one command, a `state_view` one read model, an `automation` one processor. |
| Slice status | `status` on the workflow: `created`, `planned`, `assigned`, `in_progress`, `review`, `blocked`, `done`, or `informational` |
| Owner team | `owner = team.<id>` on the workflow, and on the `bounded_context` for its events |
| Chapter summary | `description` of the `chapter`, as a multi-line string |
| Model validity for delivery | `emhcl validate --profile strict <model>` exits 0 |
