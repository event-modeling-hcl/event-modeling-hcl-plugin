# Credits and source license

The method contract (`contract/method.md`), its HCL binding, and the 32 method skills of the plugin `event-modeling-skills` restate ideas from 29 Event Modeling skills that were collected in `tmp/_to_use/` of this repository. The method skills do not name their sources, because no method skill names another skill. This file records the sources instead.

The license of the 29 source skills is unknown. Before release, run `scripts/check-source-overlap.sh` and resolve the source-license question. The script scans the contract, method skills, examples, and plugin evals for matching runs of eight words. A passing result is a text comparison, not legal clearance. Until the license question is resolved, do not describe the method content as cleared for release under Apache-2.0.

The language skill `event-modeling-hcl` comes from emhcl v0.17.0
(Apache-2.0). The retired `event-modeling` skill came from the same release.
Its edit policy now lives in K13 of `contract/method.md`. Its business guidance
is integrated into the relevant method sections, and its behavior cases live
in the plugin eval suite. These upstream contributions retain their Apache-2.0
provenance. Their integration does not clear the other restated source content.

## Contract sections

| Section | Ideas restated from |
| --- | --- |
| K1 | `eventmodeling-core-rules`, `eventmodeling-designing-event-models`, `eventmodeling-identifying-outputs`, `eventmodeling-validating-event-models` |
| K2 | `eventmodeling-core-rules`, `eventmodeling-designing-automation-chains`, `eventmodeling-identifying-inputs`, `eventmodeling-identifying-outputs`, `eventmodeling-information-completeness`, `eventmodeling-storyboarding-events` |
| K3 | `eventmodeling-core-rules`, `eventmodeling-slicing-event-models` |
| K4 | `eventmodeling-core-rules`, `eventmodeling-identifying-outputs`, `eventmodeling-orchestrating-event-modeling`, `eventmodeling-validating-event-models-checklist`, `wdyt` |
| K5 | `eventmodeling-elaborating-scenarios`, `scenario-coverage`, `wdyt` |
| K6 | `eventmodeling-elaborating-scenarios`, `eventmodeling-workshop-questions`, `summarize` |
| K7 | `eventmodeling-checking-completeness`, `eventmodeling-designing-event-models`, `eventmodeling-plotting-events`, `eventmodeling-validating-event-models` |
| K8 | `analyze-code-base`, `apply-feedback`, `data-journey`, `detect-model-drift`, `eventmodeling-checking-completeness`, `eventmodeling-core-rules`, `eventmodeling-interview-protocol`, `eventmodeling-orchestrating-event-modeling`, `summarize`, `walkthrough` |
| K9 | `analyze-code-base`, `apply-feedback`, `data-journey`, `eventmodeling-core-rules`, `eventmodeling-interview-protocol`, `summarize`, `walkthrough` |
| K10 | `detect-model-drift`, `eventmodeling-checking-completeness`, `eventmodeling-core-rules`, `eventmodeling-validating-event-models`, `eventmodeling-validating-event-models-checklist`, `stressor-analysis`, `wdyt` |
| K11 | `eventmodeling-orchestrating-event-modeling`, `eventmodeling-workshop-questions`, `wdyt` |
| K12 | `analyze-code-base`, `eventmodeling-orchestrating-event-modeling`, `summarize` |

K12 also uses the step order and gates of `eventmodeling-orchestrating-event-modeling`.

## Method skills

The names below are short names of the skills in `event-modeling-skills`, without the prefix `eventmodeling-`. The sources are folder names in `tmp/_to_use/`.

| Skill | Ideas restated from |
| --- | --- |
| applying-answers | `apply-feedback`, `eventmodeling-workshop-questions`, `wdyt` |
| applying-feedback | `apply-feedback` |
| asking-business-questions | `wdyt` |
| assessing-change-impact | `walkthrough` |
| assigning-ownership | `eventmodeling-applying-conways-law` |
| auditing-field-lineage | `eventmodeling-checking-completeness`, `eventmodeling-validating-event-models`, `eventmodeling-validating-event-models-checklist` |
| auditing-model-rules | `eventmodeling-checking-completeness`, `eventmodeling-validating-event-models`, `eventmodeling-validating-event-models-checklist` |
| bounding-streams | `eventmodeling-optimizing-stream-design` |
| brainstorming-events | `eventmodeling-brainstorming-events`, `eventmodeling-designing-event-models` |
| cataloging-roles | `eventmodeling-brainstorming-events`, `eventmodeling-core-rules`, `eventmodeling-storyboarding-events`, `eventmodeling-validating-event-models` |
| deriving-commands | `eventmodeling-designing-event-models`, `eventmodeling-identifying-inputs` |
| deriving-read-models | `eventmodeling-designing-event-models`, `eventmodeling-identifying-outputs`, `eventmodeling-orchestrating-event-modeling` |
| designing-automation-chains | `eventmodeling-core-rules`, `eventmodeling-designing-automation-chains`, `eventmodeling-identifying-inputs`, `eventmodeling-orchestrating-event-modeling` |
| detecting-code-drift | `detect-model-drift` |
| estimating-delivery | `eventmodeling-orchestrating-event-modeling` |
| explaining-flow | `walkthrough` |
| extracting-document-facts | `summarize` |
| facilitating-workshop | `eventmodeling-brainstorming-events`, `eventmodeling-elaborating-scenarios` |
| grouping-chapters | `analyze-code-base`, `eventmodeling-brainstorming-events`, `summarize` |
| mapping-lifecycles | `eventmodeling-checking-completeness`, `eventmodeling-designing-event-models`, `eventmodeling-plotting-events`, `eventmodeling-validating-event-models` |
| measuring-scenario-coverage | `scenario-coverage` |
| orchestrating-workflow | `analyze-code-base`, `eventmodeling-orchestrating-event-modeling`, `summarize` |
| plotting-timeline | `eventmodeling-brainstorming-events`, `eventmodeling-plotting-events` |
| reading-code-evidence | `analyze-code-base` |
| planning-slices | `eventmodeling-checking-completeness`, `eventmodeling-slicing-event-models` |
| storyboarding-screens | `eventmodeling-storyboarding-events` |
| stress-testing-model | `stressor-analysis` |
| tracing-data-journey | `data-journey` |
| translating-external-events | `eventmodeling-translating-external-events` |
| writing-chapter-summary | `eventmodeling-orchestrating-event-modeling`, `summarize` |
| writing-command-scenarios | `analyze-code-base`, `eventmodeling-elaborating-scenarios`, `eventmodeling-translating-external-events`, `summarize` |
| writing-read-model-scenarios | `eventmodeling-elaborating-scenarios` |
