# Reference

Use this chapter to locate exact fields and commands without repeating workflow guidance. Start a new project from source/config_templates/recursive_tree.yaml or project_catalog.yaml, then replace project metadata, paths, and categories.

| Field | Purpose |
| --- | --- |
| repository.projects_dir | Content root relative to source/config.yaml |
| generation.discovery.mode | recursive_tree or project_catalog |
| generation.navigation.order | Top-level category or directory order |
| generation.default_page | Site landing page for each language |
| generation.directory_index | Section landing page filename |
| generation.pdf_style | web, thesis, graduate, or academic |
| generation.pdf_fonts | Exact fonts required locally and in CI |

Use python build_local.py --check to check local tooling, python build_local.py --clean --no-pdf for fast web output, python build.py --validate to validate versions.json, and python build.py --clean to build every version.
