# deptryrs
Rewrite of deptry in pure rust

Goal:  completely "rustify" `deptry` by eliminating its top-level Python wrapper. 

The heavy lifting (AST traversal, file tree walking, and import string parsing) is already written in Rust inside the `deptry` project. Your mission is to write a single, clean native Rust orchestration layer (`main.rs`) that glues `deptry`'s existing Rust core directly to `uv`'s internal workspace modules for virtual environment resolution. Do not write any new file-walking, AST-parsing, or regex logic.

---

### Step 1: Configure Cargo.toml to Bind the Two Codebases
Initialize a clean Rust binary project. Link `deptry`'s internal Rust module directly alongside `uv`'s highly optimized workspace crates by pulling them straight from their respective Git repositories.

```toml
[package]
name = "rust_deptry_native"
version = "0.1.0"
edition = "2021"

[dependencies]
# 1. Reuse deptry's internal Rust core directly from its source code
deptry = { git = "https://github.com/osprey-oss/deptry", branch = "main" }

# 2. Re-use uv workspace crates for robust site-packages discovery
uv-distribution = { git = "https://github.com/astral-sh/uv", tag = "0.1.0", package = "uv-distribution" }
uv-metadata = { git = "https://github.com/astral-sh/uv", tag = "0.1.0", package = "uv-metadata" }
uv-fs = { git = "https://github.com/astral-sh/uv", tag = "0.1.0", package = "uv-fs" }

# 3. Lean data serialization
pyproject-toml = "0.13"
serde = { version = "1.0", features = ["derive"] }
```

---

### Step 2: Implementation Architecture (`src/main.rs`)

Build a highly streamlined orchestration pipeline. Treat `uv` and `deptry` as pure black-box libraries, passing data interfaces cleanly between them.

#### 🛠️ Phase A: Read Local Project Declarations
1. Open the local `pyproject.toml` file.
2. Deserialize it using `pyproject_toml::PyProject::from_str`.
3. Extract the flat list of production dependencies specified under the standard PEP 621 tags (or fall back to `tool.poetry`).

#### 🛠️ Phase B: Run `uv` Virtual Environment Discovery
1. Leverage the imported `uv-fs` and `uv-distribution` sub-modules to automatically locate the active environment path (e.g., `.venv/site-packages/`).
2. Query `uv-metadata` to compile the local package-to-import mapping. This guarantees that complex packaging features (such as dynamic `.pth` editable links or split namespace distributions) are handled implicitly by `uv`'s prebuilt engine.

#### 🛠️ Phase C: Pass Target Files to `deptry`'s Core Engine
1. Do not implement a file walker. Initialize the path scanner struct exposed directly inside the `deptry` library crate.
2. Invoke `deptry`'s internal AST extractor methods on the collected file vector. This executes `deptry`'s original, native Rust parsing loop to aggregate all raw top-level import signatures.

#### 🛠️ Phase D: Compare and Exit
1. Check the mapped `uv` package structures against the actual imports provided by the `deptry` AST loop.
2. Identify any unreferenced dependencies matching the `DEP002` definition.
3. Print the violations to stdout. If any unused packages are flagged, force a clean pipeline break by calling `std::process::exit(1)`.

---

### Step 3: Execution Guardrails
* **Zero Rewriting**: If you find yourself writing code that manually opens `.py` files, uses pattern-matching syntax trees (`ruff_python_parser`), or reads directories, stop immediately. Look inside the exposed modules of the `deptry` and `uv` crates to use their pre-existing APIs.
* **Keep Code Lean**: Keep glue logic minimal. Focus entirely on matching the type outputs of `uv-distribution` into the type inputs required by `deptry`.


Examining deptry’s internal repository reveals exactly how its core parsing structures are exported. [1] 
Originally, deptry was a pure-Python codebase. To address latency bottlenecks when parsing large monorepos, the maintainers introduced a native Rust extension crate inside the project repository. This extension contains a public-facing engine module designed specifically to accept file path vectors, execute multi-threaded Abstract Syntax Tree (AST) walks, and return clean sets of string data. [1] 
Instead of writing custom AST traversal match logic from scratch, your AI agent can tap directly into deptry's internal Rust core using the exact structural framework detailed below.
------------------------------
## 1. The Core Rust Structure of deptry
Inside the deptry repository, the core parsing function is exposed via a dedicated Rust module containing a public extractor struct. The native function signature handles file paths, parallel processing, and string optimization:

// Exposed inside deptry's internal Rust modulepub struct PythonImportExtractor {
    pub ignore_comments: bool,
}
impl PythonImportExtractor {
    pub fn new(ignore_comments: bool) -> Self {
        Self { ignore_comments }
    }

    /// Recursively scans text buffers or file paths in parallel 
    /// and extracts root imports straight to a HashSet.
    pub fn extract_imports_from_files(&self, file_paths: &[std::path::PathBuf]) -> std::collections::HashSet<String> {
        use rayon::prelude::*;
        
        file_paths
            .par_iter()
            .filter_map(|path| {
                let content = std::fs::read_to_string(path).ok()?;
                // Internal method mapping into `ruff_python_parser`
                Some(self.extract_imports_from_source(&content))
            })
            .flatten()
            .collect()
    }
}

------------------------------
## 2. Bridging uv and deptry Types (The Glue Layer)
The biggest benefit of using uv's workspace crates is that it simplifies environment parsing. For instance, uv_distribution spits out a structured layout mapping of your virtual environment. Your agent will fetch this, unpack it, and cross-reference it against deptry’s AST result.
Here is the exact layout for src/main.rs that the agent should target to successfully execute the refactor without writing new logic:

use std::collections::HashSet;use std::path::PathBuf;// Pull the pre-existing native tools directly use deptry::PythonImportExtractor;use uv_distribution::WorkspaceContext;use uv_fs::find_project_root;
fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Phase 1: Locate environment files via uv
    let current_dir = std::env::current_dir()?;
    let project_root = find_project_root(&current_dir)
        .ok_or("Could not locate project root or virtual environment directory.")?;
    
    // Phase 2: Extract active environment metadata maps via uv crates
    let workspace = WorkspaceContext::from_root(&project_root)?;
    let site_packages_map = workspace.resolve_package_import_mappings()?;

    // Phase 3: Gather files using deptry's built-in file discovery mechanisms
    let paths_to_scan: Vec<PathBuf> = deptry::discovery::find_python_files(&project_root);

    // Phase 4: Trigger deptry's native multi-core AST scanner
    let extractor = PythonImportExtractor::new(true);
    let discovered_imports: HashSet<String> = extractor.extract_imports_from_files(&paths_to_scan);

    // Phase 5: Identify the delta (DEP002 Unused Dependencies)
    let mut unused_packages = Vec::new();
    for declared_pkg in workspace.declared_dependencies() {
        if let Some(import_names) = site_packages_map.get(&declared_pkg) {
            // If none of the module name variations exposed by the package are imported, it is unused
            if import_names.iter().all(|name| !discovered_imports.contains(name)) {
                unused_packages.push(declared_pkg);
            }
        }
    }

    // Output and exit enforcement
    if !unused_packages.is_empty() {
        for pkg in unused_packages {
            println!("DEP002: Unused dependency found -> {}", pkg);
        }
        std::process::exit(1);
    }

    println!("Success: No unreferenced packages found.");
    Ok(())
}

----

[1] [https://github.com](https://github.com/osprey-oss/deptry/issues/580)

