# `config.yaml` templates

This directory contains two complete configuration templates. Choose the model that matches the repository, copy it to `source/config.yaml`, then update project metadata, source paths, and categories.

| Template | Repository type | Source selection | Navigation |
| --- | --- | --- | --- |
| `recursive_tree.yaml` | Tutorials, manuals, and knowledge bases | Recursively synchronize supported files under `projects_dir` | Preserve the source directory tree |
| `project_catalog.yaml` | SDK, BSP, and example collections | Synchronize only selected project entry READMEs and `asset_globs` | Group projects by `categories` |

## Usage

```powershell
# Windows PowerShell, from the repository root
Copy-Item source/config_templates/recursive_tree.yaml source/config.yaml
cd source
python build_local.py --clean
```

```bash
# Linux/macOS, from the repository root
cp source/config_templates/recursive_tree.yaml source/config.yaml
cd source
python build_local.py --clean
```

Before replacing an existing `source/config.yaml`, preserve its project identity, copyright, giscus, and custom font settings.

## `recursive_tree`

This mode implements the one-README-per-directory documentation model:

- Synchronize every file allowed by `generation.sync_extensions` recursively.
- Prefer the README configured by `generation.directory_index` in each directory; generate an index when absent.
- Keys in `generation.navigation.order` should match top-level documentation directories and `categories` keys.
- `generation.navigation.directory_order` maps parent paths relative to `projects_dir` to ordered direct-child directory names. HTML and PDF share this order; unlisted children follow in natural order. Adapt the template's six application directories to your repository.
- HTML animations and CSS/JS dependencies are included in `sync_extensions`, preserving relative paths.
- PDF retains each directory README title but omits navigation prose; a README-only directory is treated as content.
- Root READMEs under `projects_dir` are authoritative language markers. Repository-root and directory markers are combined only when no root marker exists.

## `project_catalog`

This mode is designed for SDK/BSP repositories containing source code, packages, and example projects:

- `categories.*.patterns` selects project roots. Patterns without `/` match only first-level directories.
- Nested projects require explicit relative paths and are never inferred from recursive README searches.
- Each project contributes only `generation.discovery.entry_files` and `asset_globs`.
- The template includes project-root HTML/HTM/CSS/JS and `figures/**`. Add explicit globs such as `demos/**` for dependencies in other directories; source trees are not automatically included.
- `navigation.order` controls categories; directory-tree `directory_order` does not reorder projects within categories.
- A project entry README is content in both HTML and PDF; vendor and package READMEs remain excluded.
- Projects may have partial language coverage. The switch appears only when the final catalog contains both languages.
- Keep `unmatched_projects: error` and `duplicate_categories: error` for deterministic output.

Strict catalog builds reject:

- Patterns that match no project directory.
- Projects assigned to multiple categories.
- Unknown categories in navigation order.
- Selected projects without any configured entry README.
- Paths escaping `projects_dir`.
- Local README images that are missing or excluded by `asset_globs`.

## Shared settings

| Setting | Purpose |
| --- | --- |
| `repository.projects_dir` | Source directory relative to `source/config.yaml`, commonly `../projects` or `../project` |
| `generation.default_page` | Per-language site home; repository-root README fallback also synchronizes its referenced local images |
| `generation.default_language` | Preferred language selected from actually available languages |
| `generation.navigation.order` | Display order for top-level directories or categories |
| `generation.navigation.maxdepth` | Maximum global document-tree depth; `-1` keeps every nested directory reachable |
| `generation.navigation.titles_only` | Keep section headings out of the global tree (recommended: `true`) |
| `generation.navigation.show_local_toc` | Show the current article's H2/H3 outline in the right reading rail |
| `generation.pdf_fonts` | Exact fonts required locally and in CI; missing fonts fail without silent substitution |

`generation.mode` and `generation.output_structure` have been removed and are rejected. Migrate to `generation.discovery.mode`, `generation.navigation.mode`, and `generation.navigation.order`.

## Switching modes

Update `generation.discovery.mode`, `generation.navigation.mode`, and category rules together, not just the legacy `generation.mode`. The supported pairs are `recursive_tree` + `directory_tree` and `project_catalog` + `categories`. For a project catalog, configure `entry_files`, `asset_globs`, and `categories.*.patterns`, and adjust `repository.projects_dir`. Use `--clean` as shown above when switching. The generated-file manifest removes files synchronized by the previous mode without modifying original project documents.
