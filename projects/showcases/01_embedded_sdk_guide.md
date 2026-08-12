# Showcase: Embedded SDK Guide

A sensor SDK needs installation, initialization, data capture, error code, and board-level diagnostic documentation. Readers follow a learning path, so use recursive_tree and let the directory hierarchy become the navigation hierarchy.

~~~text
projects/
├── getting_started/
├── api_reference/
└── troubleshooting/
~~~

Installation pages state supported systems, toolchains, and minimum SDK versions. API pages combine parameter tables with minimal runnable code. Diagnostics follow symptom, evidence, cause, and repair rather than a module-name dump. Matching Chinese and English names keep the reading context during language switching.

Run python build_local.py --clean --no-pdf --serve and inspect sidebar continuity, code blocks, images, and counterpart routes. Before release, run a full PDF build and verify long tables and code remain in bounds.
