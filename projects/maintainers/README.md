# Maintainer Guide

Content authors maintain projects; builder maintainers own source modules for discovery, synchronization, navigation, HTML, PDF, versions, and tests. Every new feature should state how it affects the content catalog, language behavior, HTML output, PDF output, and CI validation.

| Module | Responsibility |
| --- | --- |
| DocumentCatalog | Discover documents and assets; enforce path and category rules |
| FileProcessor and IndexGenerator | Synchronize content; generate language-aware navigation |
| html_builder | Build language sites and a stable entry point |
| pdf_builder and pdf_environment | Validate PDF tooling, build, and verify files |
| build.py and build_manager | Resolve version matrix, isolate worktrees, collect outputs |

When changing discovery or navigation, cover recursive_tree, project_catalog, Chinese, English, bilingual behavior, and missing-translation fallbacks. When changing PDFs, add unit coverage and validate a real output with XeLaTeX and configured fonts. Prefer sharing DocumentCatalog over independently scanning the filesystem in each output path.
