# Local Build Workflow

build_local.py is the local entry point for one version. It supports cleanup, dependency checks, static serving, port selection, PDF skipping, disabled auto-installation, and branch validation.

| Option | Purpose |
| --- | --- |
| --clean | Remove old HTML before the build |
| --serve | Start a static server after the build |
| --port 8000 | Select the server port |
| --no-pdf | Skip XeLaTeX and focus on web feedback |
| --check | Check dependencies and build environment |
| --no-auto-install | Report instead of installing Python or PDF dependencies |
| --check-branch | Validate the current branch against the version configuration |

After a build, check the redirecting home page, sidebars, search, deep links, language switching, and static images. Do not stop at the home page: directory landings, third-level pages, and missing-translation fallbacks expose most path errors.

On desktop, verify the left global tree, center article, and right local outline. Resize the window to confirm that the article does not jump between widths and that the outline moves below the article only when the columns no longer fit. h2/h3 outline items should remain nested and indented, clicks should scroll smoothly and update the active item, and switching articles should preserve the expanded navigation path.
