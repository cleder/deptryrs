<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Architecture](#architecture)
  - [Pipeline](#pipeline)
  - [Phases](#phases)
    - [Phase A — Read project declarations](#phase-a--read-project-declarations)
    - [Phase B — Virtual-environment discovery](#phase-b--virtual-environment-discovery)
    - [Phase C — Import extraction](#phase-c--import-extraction)
    - [Phase D — Delta and exit](#phase-d--delta-and-exit)
  - [Key constraint](#key-constraint)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Architecture

deptryrs is a thin orchestration layer. It owns no parsing, file-walking, or environment-discovery
logic — all of that is delegated to upstream crates.

## Pipeline

```text {mermaid}
flowchart LR
    A[pyproject.toml] -->|pyproject-toml crate| B[declared deps]
    C[.venv/] -->|uv-distribution / uv-metadata| D[package→import map]
    E[Python source files] -->|deptry core| F[discovered imports]
    B & D & F --> G{compare}
    G -->|unused| H[DEP002 violations → stdout, exit 1]
    G -->|all used| I[success, exit 0]
```

## Phases

### Phase A — Read project declarations

`pyproject_toml::PyProject::from_str` deserialises `pyproject.toml` and extracts the flat list
of production dependencies (PEP 621 or `tool.poetry` fallback).

### Phase B — Virtual-environment discovery

`uv-fs` and `uv-distribution` locate the active environment (`.venv/site-packages/`).
`uv-metadata` compiles the package-to-import-name mapping, handling editable installs and
namespace packages transparently.

### Phase C — Import extraction

deptry's built-in path scanner discovers Python source files; its Rust AST extractor (backed by
`ruff_python_parser`) collects all top-level import names in parallel via rayon.

### Phase D — Delta and exit

Declared packages whose import names are absent from the discovered set are flagged as DEP002.
Results go to stdout; a non-empty violation list causes `process::exit(1)`.

## Key constraint

:::{important}
deptryrs MUST NOT implement its own file-walking, AST-parsing, or virtual-environment discovery.
If an upstream API is insufficient, open an issue there — do not duplicate the logic here.
:::
