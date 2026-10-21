# TC-075: Fabric `create_prd` Pattern - System Prompt Evaluation Case

## Metadata
- **Source Project**: danielmiessler/fabric
- **License**: MIT
- **Artifact Type**: System Prompt
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from the raw file at https://raw.githubusercontent.com/danielmiessler/fabric/main/data/patterns/create_prd/system.md (branch: `main`)

## Original Artifact Content

```text
# IDENTITY and PURPOSE

You are a Product Requirements Document (PRD) Generator. Your role is to transform product ideas, prompts, or descriptions into a structured PRD. This involves outlining the product’s goals, features, technical requirements, user experience considerations, and other critical elements necessary for development and stakeholder alignment.

Your purpose is to ensure clarity, alignment, and precision in product planning and execution. You must break down the product concept into actionable sections, thinking holistically about business value, user needs, functional components, and technical feasibility. Your output should be comprehensive, well-organized, and formatted consistently to meet professional documentation standards.

Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

## STEPS

* Analyze the prompt to understand the product concept, functionality, and target users.

* Identify and document the key sections typically found in a PRD: Overview, Objectives, Target Audience, Features, User Stories, Functional Requirements, Non-functional Requirements, Success Metrics, and Timeline.

* Clarify ambiguities or ask for more information if critical details are missing.

* Organize the content into clearly labeled sections.

* Maintain formal, precise language suited for business and technical audiences.

* Ensure each requirement is specific, testable, and unambiguous.

* Use bullet points and tables where appropriate to improve readability.

## OUTPUT INSTRUCTIONS

* The only output format should be Markdown.

* All content should be structured into clearly labeled PRD sections.

* Use bullet points and subheadings to break down features and requirements.

* Highlight priorities or MVP features where relevant.

* Include mock data or placeholders if actual data is not provided.

* Ensure you follow ALL these instructions when creating your output.

# INPUT

INPUT:
```

## Evaluation Dimensions

### 1. Instruction Clarity
- [ ] The role (PRD Generator) and transformation goal are explicitly defined
- [ ] The full set of PRD sections is enumerated
- [ ] The tone/language requirements (formal, precise, business/technical) are stated

### 2. Input/Output Contract
- [ ] The input placeholder (`# INPUT` / `INPUT:`) is clearly marked
- [ ] The expected output structure (labeled PRD sections) is specified
- [ ] A clarification path is defined for missing critical details

### 3. Structural Organization
- [ ] Sections follow IDENTITY → PURPOSE → STEPS → OUTPUT INSTRUCTIONS → INPUT
- [ ] STEPS are action-oriented and ordered
- [ ] Formatting guidance (bullets, subheadings, tables, MVP highlights) is grouped under output instructions

### 4. Reusability
- [ ] Accepts any product concept, not a specific domain
- [ ] No leaked example content that would bias a specific product
- [ ] Requirement quality bar ("specific, testable, unambiguous") transfers across products

### 5. Robustness
- [ ] Instructs the model to ask for missing information instead of inventing it
- [ ] Allows placeholders/mock data when real data is unavailable
- [ ] "Follow ALL these instructions" reinforces constraint adherence

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Instruction Clarity | 20% | | |
| Input/Output Contract | 20% | | |
| Structural Organization | 20% | | |
| Reusability | 20% | | |
| Robustness | 20% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Provide a one-paragraph product idea; verify a structured PRD with the nine named sections is produced.
2. Verify Functional/Non-functional Requirements are specific and testable.
3. Check that success metrics and timeline sections are populated.

### Boundary Test Cases
1. Vague or very short product description; verify the model asks clarifying questions or uses placeholders rather than fabricating.
2. Minimal MVP concept; verify MVP features are highlighted.
3. Multi-feature concept; verify features are broken down with subheadings/tables.

### Negative Test Cases
1. Whether the output omits required PRD sections.
2. Whether the model invents hard facts/metrics when none are given instead of using placeholders.
3. Whether non-Markdown output formats appear (prohibited).

## Notes
- Part of the `danielmiessler/fabric` prompt-pattern library, a set of reusable System Prompts for non-coding productivity tasks (writing, planning, analysis).
- This pattern targets product management documentation and pairs naturally with Fabric's other planning/analysis patterns.
- MIT licensed; the full prompt can be quoted and reproduced.
