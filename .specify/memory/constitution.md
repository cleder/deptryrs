<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [deptryrs Constitution](#deptryrs-constitution)
  - [Core Principles](#core-principles)
    - [I. Test-First (NON-NEGOTIABLE)](#i-test-first-non-negotiable)
    - [II. Documentation-First](#ii-documentation-first)
    - [III. Zero Rewriting of Upstream Cores](#iii-zero-rewriting-of-upstream-cores)
    - [IV. Minimal Glue Layer](#iv-minimal-glue-layer)
    - [V. Correctness Over Performance](#v-correctness-over-performance)
  - [Technology Stack](#technology-stack)
  - [Development Workflow](#development-workflow)
  - [Governance](#governance)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<!-- SYNC IMPACT REPORT
Version: [unversioned template] → 1.0.0
Version bump rationale: MINOR — initial fill of all placeholders; first concrete constitution.
Modified principles: none (initial authoring from blank template)
Added sections:
  - Core Principles (I–V): Test-First, Documentation-First, Zero Rewriting, Minimal Glue, Correctness
  - Technology Stack
  - Development Workflow
  - Governance
Removed sections: none
Templates updated:
  ✅ .specify/templates/plan-template.md — Constitution Check gates made concrete
  ✅ .specify/templates/spec-template.md — no changes required; template already supports TDD
  ✅ .specify/templates/tasks-template.md — no changes required; TDD ordering already enforced
  ✅ No commands directory found — nothing to update
Deferred TODOs: none
-->

# deptryrs Constitution

## Core Principles

### I. Test-First (NON-NEGOTIABLE)

All implementation MUST be preceded by failing tests. The Red-Green-Refactor cycle is strictly
enforced:

1. Write the test.
2. Confirm the test fails (red).
3. Present failing tests to the user for approval before writing any implementation.
4. Implement only enough code to make the test pass (green).
5. Refactor without breaking tests.

No feature or bug fix may be merged unless tests were written first and demonstrably failed before
the implementation was added. Both unit and integration tests are required where applicable.
Skipping TDD requires explicit written justification from the project owner.

### II. Documentation-First

Documentation is a first-class citizen and MUST be written alongside — or before — the code it
describes. All project documentation MUST be authored in MyST Markdown format to enable rich
cross-referencing, directives, and Sphinx/Jupyter Book compatibility.

Rules:

- Every public API surface MUST have MyST-formatted doc comments or an accompanying `.md` file.
- Tutorials, how-to guides, and architecture notes MUST live under `docs/` in MyST format.
- Documentation changes are REQUIRED in the same PR/commit as the code they describe.
- A feature is not complete until `make docs` passes without warnings.
- Inline comments explain *why*, never *what*; the code and MyST docs handle the what.

### III. Zero Rewriting of Upstream Cores

deptryrs MUST NOT reimplement logic that already exists in the `deptry` or `uv` crates. Specifically:

- No new file-walking or directory-scanning logic.
- No new AST-parsing or regex-based import extraction.
- No new virtual-environment discovery code.

If an upstream API is insufficient, the correct response is to open an issue upstream or write a
thin adapter — never to duplicate the logic locally. Any apparent exception MUST be approved
explicitly and recorded in the Complexity Tracking table of the relevant plan.

### IV. Minimal Glue Layer

The orchestration layer (`main.rs` and supporting modules) MUST remain as small as possible.
Every line of glue code MUST be justifiable as a necessary bridge between `deptry` and `uv` APIs.

- Abstractions are forbidden unless they eliminate demonstrable, current repetition.
- YAGNI: Do not design for hypothetical future requirements.
- Three similar lines are preferable to a premature abstraction.
- Complexity added without a specific current need MUST be documented in the PR description
  and in the `plan.md` Complexity Tracking table before the PR is opened.

### V. Correctness Over Performance

The primary obligation of deptryrs is accurate dependency detection (DEP002 and related rules).
Optimisation MUST NOT be pursued at the cost of correctness or test coverage.

- All changes to dependency-resolution logic MUST include regression tests covering previously
  detected violations.
- Performance improvements are welcome only after they are validated by benchmarks and confirmed
  to produce identical observable output.
- Exit code semantics (0 = clean, 1 = violations found) are contractual and MUST NOT change
  without a major version bump.

## Technology Stack

- **Language**: Rust 2021 edition; `cargo test` is the primary test runner.
- **Dependency checker core**: `deptry` crate (upstream Git dependency, pinned by tag or commit).
- **Virtual environment resolution**: `uv-distribution`, `uv-metadata`, `uv-fs` upstream crates.
- **Python project metadata**: `pyproject-toml` crate.
- **Documentation toolchain**: MyST Markdown rendered via Sphinx or Jupyter Book;
  `make docs` MUST pass without warnings before any PR is merged.
- **CI**: GitHub Actions (see `.github/workflows/`). Tests, docs, and lints MUST all be green
  before merge.

## Development Workflow

1. **Spec before code**: Every non-trivial change starts with a spec or plan document under
   `specs/`.
2. **Tests before implementation**: Write failing tests; confirm they fail; get user approval;
   then implement. Never reverse this order.
3. **Document alongside code**: MyST docs updated in the same commit as the code change.
4. **PR checklist** — all MUST pass:
   - [ ] Failing tests written and reviewed before implementation began (TDD gate).
   - [ ] All existing and new `cargo test` tests pass.
   - [ ] Documentation updated; `make docs` is clean (docs gate).
   - [ ] No new file-walking, AST-parsing, or venv-discovery code introduced (zero-rewrite gate).
   - [ ] Complexity Tracking table updated if any Constitution gate is triggered (glue gate).
   - [ ] Exit-code contract unchanged, or a major version bump is included (correctness gate).
5. **Merge policy**: Squash-merge to `main`; every commit on `main` MUST be green in CI.

## Governance

This constitution supersedes all other development practices for deptryrs. When any other
guideline, convention, or convenience conflicts with a principle above, this document takes
precedence.

Amendment procedure:

1. Open a PR proposing changes to this file with the version bump (MAJOR/MINOR/PATCH) stated
   in the PR description.
2. Provide a rationale and, for MAJOR bumps, a migration plan.
3. At least one reviewer MUST approve the amendment.
4. Update `LAST_AMENDED_DATE` and `CONSTITUTION_VERSION` in the same PR.
5. Merge only after CI is green and the Sync Impact Report comment is updated.

All PRs and code reviews MUST verify compliance with the five principles above. Violations found
during review MUST be resolved before merge — not deferred unless explicitly noted in the
Complexity Tracking table with an owner and deadline.

Use the active feature's `plan.md` for runtime development guidance during implementation.

**Version**: 1.0.0 | **Ratified**: 2026-06-27 | **Last Amended**: 2026-06-27
