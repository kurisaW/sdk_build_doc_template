# Overview

This template is for technical documentation that must be maintained, published, and trusted over time. Markdown is not treated as disposable web input: content directories, navigation, language, PDFs, and the release environment form one engineering system.

| Design goal | Mechanism | Benefit |
| --- | --- | --- |
| Separate content from tooling | projects holds content; source holds the builder | Authors do not edit generated copies |
| Two content models | recursive_tree and project_catalog | Supports manuals and SDK collections |
| One source of truth for outputs | DocumentCatalog drives HTML, PDFs, and assets | Fewer web/PDF mismatches |
| Local and CI parity | Shared configuration and font checks | Previews resemble releases |
| Traceable releases | versions.json drives isolated worktrees | Stable branches stay isolated |

## Page Information Architecture

The Web page has three explicit responsibilities: the global book tree, the article, and the current-page outline.

| Region | Content | Behavior |
| --- | --- | --- |
| Left tree | The complete book tree and article entry points | Unlimited directory depth; one expanded branch per level; expansion paths survive page changes |
| Center article | The current document | clamp keeps the reading width stable; the layout stacks only when all columns no longer fit |
| Right outline | The current page h2/h3 headings | page_outline.js extracts plain text and nests levels; it is sticky on desktop and follows the article on narrow screens |

The global tree answers “where am I in the book?”, while the local outline answers “which sections are in this article?”. Keeping these concerns separate prevents deep directories from consuming the reading column.

A simple static site only turns files into pages. A documentation product must also prevent missing navigation, escaping links, mixed-language search, non-reproducible PDFs, and CI-only failures. This template fails explicitly rather than silently degrading. Continue with the [Capability Map](01_capability_map.md), or validate it through [Quick Start](../getting_started/README.md).
