# Capability Map and Validation Boundaries

The important part is not the number of features. Every feature has an explicit input, output, and failure boundary.

| Stage | Input | Output | Release gate |
| --- | --- | --- | --- |
| Content discovery | Documents and assets in projects | Validated DocumentCatalog | Escaping paths, missing local images, conflicting project rules |
| HTML build | Catalog and Sphinx configuration | Isolated Chinese and English sites | Language landing page or navigation failure |
| PDF build | The same catalog and LaTeX configuration | One or two downloadable PDFs | XeLaTeX, font, or PDF-validity failure |
| Versioned build | versions.json and Git branches | Isolated version directories | Invalid branch or version definition |
| GitHub release | Validated artifacts | Artifact and GitHub Pages | Failed pull-request validation blocks deployment |

The web output includes search, dark mode, language switching, a version menu, edit links, PDF downloads, and optional giscus discussion. PDFs retain covers, contents, headers, page numbers, bookmarks, chapter breaks, code, tables, images, and WebP conversion. Select a repository model in [Content Models](../content_models/README.md).
