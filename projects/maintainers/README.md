# Maintainer Guide

Content authors maintain projects; builder maintainers own source modules for discovery, synchronization, navigation, HTML, PDF, versions, and tests. Every new feature should state how it affects the content catalog, language behavior, HTML output, PDF output, and CI validation.

| Module | Responsibility |
| --- | --- |
| DocumentCatalog | Discover documents and assets; enforce path and category rules |
| FileProcessor and IndexGenerator | Synchronize content; generate language-aware navigation |
| html_builder | Build language sites and a stable entry point |
| pdf_builder and pdf_environment | Validate PDF tooling, build, and verify files |
| build.py and build_manager | Resolve version matrix, isolate worktrees, collect outputs |

## Web Navigation Boundaries

layout.html owns structure and keeps article headings out of the global toctree. custom.css sizes the article and outline from the content container, stacking only when space is insufficient. page_outline.js consumes only the current article h2/h3 headings, emits a plain-text nested outline, and tracks reading progress. navigation_state.js owns the left-tree expansion path and restores it across document and anchor navigation. Changes to any of these modules should be checked at desktop three-column, narrow single-column, deep-directory, and in-page-anchor states.

When changing discovery or navigation, cover recursive_tree, project_catalog, Chinese, English, bilingual behavior, and missing-translation fallbacks. When changing PDFs, add unit coverage and validate a real output with XeLaTeX and configured fonts. Prefer sharing DocumentCatalog over independently scanning the filesystem in each output path.
