<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [From source](#from-source)
    - [Running against a project](#running-against-a-project)
  - [Output](#output)
  - [Exit codes](#exit-codes)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Getting Started

## Prerequisites

- Rust 2024 edition toolchain (`rustup` recommended)
- A Python project managed by [uv](https://github.com/astral-sh/uv) with a `pyproject.toml`

## Installation

### From source

```{code-block} shell
git clone https://github.com/christianledermann/deptryrs
cd deptryrs
cargo build --release
```

The binary lands at `target/release/deptryrs`.

### Running against a project

Run deptryrs from the root of your Python project (where `pyproject.toml` lives):

```{code-block} shell
cd /path/to/your/python-project
/path/to/deptryrs
```

## Output

Unused dependencies are printed one per line:

```{code-block} text
DEP002: Unused dependency found -> requests
DEP002: Unused dependency found -> httpx
```

The process exits with code `1` when violations are found, making it suitable as a CI gate.

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | No unused dependencies detected |
| `1` | One or more DEP002 violations found |
