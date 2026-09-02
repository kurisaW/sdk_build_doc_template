# Reference

Use this chapter to locate exact fields and commands without repeating workflow guidance. Start a new project from source/config_templates/recursive_tree.yaml or project_catalog.yaml, then replace project metadata, paths, and categories.

| Field | Purpose |
| --- | --- |
| repository.projects_dir | Content root relative to source/config.yaml |
| generation.discovery.mode | recursive_tree or project_catalog |
| generation.navigation.order | Top-level category or directory order |
| generation.navigation.maxdepth | Global tree depth; -1 keeps the complete directory tree |
| generation.navigation.titles_only | Whether the global tree shows titles only |
| generation.navigation.show_local_toc | Whether to render the current page h2/h3 outline |
| generation.default_page | Site landing page for each language |
| generation.directory_index | Section landing page filename |
| generation.pdf_style | web, thesis, graduate, or academic |
| generation.pdf_fonts | Exact fonts required locally and in CI |

Use python build_local.py --check to check local tooling, python build_local.py --clean --no-pdf for fast web output, python build.py --validate to validate versions.json, and python build.py --clean to build every version.

## Page Implementation

| File | Responsibility |
| --- | --- |
| source/_templates/layout.html | Mounts the global tree, article container, and local outline |
| source/_static/custom.css | Defines column sizing, container queries, level indentation, and narrow-screen stacking |
| source/_static/page_outline.js | Extracts h2/h3 headings, builds a plain-text nested outline, and tracks reading progress |
| source/_static/navigation_state.js | Preserves the unique expanded path across document and anchor navigation |
