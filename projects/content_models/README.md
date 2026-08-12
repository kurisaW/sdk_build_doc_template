# Content Models

Which files are included and how a sidebar is displayed are different questions. The template provides two explicit models so a handbook does not accidentally publish third-party READMEs, while an SDK collection is not forced into a linear chapter structure.

| Model | Best for | Discovery | Navigation |
| --- | --- | --- | --- |
| recursive_tree | Tutorials, product manuals, knowledge bases | Recursively synchronizes allowed documents and assets | Preserves the directory tree |
| project_catalog | SDKs, BSPs, sample-project collections | Includes only matching project entry READMEs and declared assets | Organizes by business category |

Both models pass an exact file list through DocumentCatalog. HTML, PDFs, language detection, and asset validation share it, preventing divergent web and PDF contents. Use [Model Selection](01_model_selection.md) to choose.
