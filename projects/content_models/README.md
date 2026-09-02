# Content Models

Which files are included and how a sidebar is displayed are different questions. The template provides two explicit models so a handbook does not accidentally publish third-party READMEs, while an SDK collection is not forced into a linear chapter structure.

| Model | Best for | Discovery | Navigation |
| --- | --- | --- | --- |
| recursive_tree | Tutorials, product manuals, knowledge bases | Recursively synchronizes allowed documents and assets | Preserves the directory tree |
| project_catalog | SDKs, BSPs, sample-project collections | Includes only matching project entry READMEs and declared assets | Organizes by business category |

Both models pass an exact file list through DocumentCatalog. HTML, PDFs, language detection, and asset validation share it, preventing divergent web and PDF contents. Use [Model Selection](01_model_selection.md) to choose.

## Global Tree and Article Outline

The discovery model decides which documents enter the site; navigation decides how those documents appear in the left tree. Article headings are handled separately: generation.navigation.maxdepth set to -1 keeps deep directory entries available, titles_only prevents the global tree from recursively listing article sections, and show_local_toc enables the current page h2/h3 tree on the right.

page_outline.js builds a nested list from heading anchors and plain text, without reusing Markdown or code-highlight nodes. navigation_state.js enforces one expanded branch per level and restores the path after document or in-page anchor navigation.
