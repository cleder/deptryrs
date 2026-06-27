---
myst:
  html_meta:
    description: "deptryrs — pure-Rust rewrite of the deptry Python dependency checker"
---

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [deptryrs](#deptryrs)
  - [Why deptryrs?](#why-deptryrs)
  - [Quick start](#quick-start)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# deptryrs

A pure-Rust orchestration layer for [deptry](https://github.com/osprey-oss/deptry) that
eliminates the top-level Python wrapper. It glues deptry's existing Rust core directly to
uv's workspace crates for virtual-environment resolution.

## Why deptryrs?

- **Zero Python at runtime** — no interpreter startup, no venv bootstrap overhead.
- **Reuses upstream cores** — no duplicated file-walking, AST-parsing, or import-extraction logic.
- **Minimal glue** — `main.rs` is the only new code; everything else comes from `deptry` and `uv`.

## Quick start

```{code-block} shell
cargo build --release
./target/release/deptryrs
```

Exit codes: `0` = no unused dependencies, `1` = DEP002 violations found.

```text {toctree}
:maxdepth: 2
:caption: Contents

getting-started
architecture
contributing
```
