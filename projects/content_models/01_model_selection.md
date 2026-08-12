# Choosing a Recursive Tree or Strict Project Catalog

Choose recursive_tree when the directory hierarchy is the reader's learning path. It recursively synchronizes Markdown, RST, and assets, using directory READMEs as chapter pages. It suits installation guides, API manuals, product tutorials, and architecture knowledge bases.

Choose project_catalog when a repository contains source code, vendor packages, build outputs, and several independent examples. Use categories.*.patterns to select project roots, then include only declared entry_files and asset_globs.

Strict mode rejects empty matches, duplicate categories, missing entry READMEs, escaping paths, and images that were not synchronized. Its value is a provable answer to both “what was published?” and “what was excluded?”. Select discovery first, then configure navigation; do not use naming tricks to mix these responsibilities.
