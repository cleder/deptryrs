<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Contributing](#contributing)
  - [Development workflow](#development-workflow)
  - [Building](#building)
  - [Building the docs](#building-the-docs)
  - [PR checklist](#pr-checklist)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Contributing

## Development workflow

All contributions MUST follow the project constitution (`.specify/memory/constitution.md`).
The short version:

1. **Write failing tests first** — confirm they fail, then implement.
2. **Update docs in the same commit** — a change without docs is not done.
3. **Keep the glue layer small** — no new file-walking, AST, or venv code.

## Building

```{code-block} shell
cargo build
cargo test
```

## Building the docs

Install the doc dependencies (a virtualenv is recommended):

```{code-block} shell
pip install -r docs/requirements.txt
make docs
```

The built HTML lands in `docs/_build/html/`. Open `index.html` in a browser to review.

## PR checklist

Before opening a PR confirm:

- [ ] Failing tests were written first and reviewed before implementation.
- [ ] `cargo test` passes.
- [ ] `make docs` passes without warnings.
- [ ] No new file-walking, AST-parsing, or venv-discovery code was introduced.
- [ ] The Complexity Tracking table in `plan.md` is updated for any justified exception.
