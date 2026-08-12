# First Local Build

Run these commands from source. The script reads config.yaml, checks pinned Python dependencies, synchronizes projects, generates navigation, and builds each language site independently.

~~~bash
python build_local.py --check
python build_local.py --clean --no-pdf
python build_local.py --clean --no-pdf --serve --port 8000
~~~

| Path | Purpose |
| --- | --- |
| source/_build/html/index.html | Stable local entry point that redirects to the default language |
| source/_build/html/ | HTML, search index, and static assets |
| source/_build/html/_static/ | Downloadable PDFs and runtime page assets |
| source/_build/latex/ | PDF intermediates, removed after a successful build |

Use --no-auto-install in controlled environments to report dependency differences without changing the environment. Use --clean to prevent removed pages from persisting in old navigation or search outputs. If HTML succeeds but PDF fails, install the exact configured fonts as described in [PDF Delivery](../build_outputs/02_pdf_delivery.md).
