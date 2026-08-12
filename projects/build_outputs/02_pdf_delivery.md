# PDF Delivery: Typesetting and Environment Are Inputs

PDFs are not printed web pages. The template fixes the route to Sphinx LaTeX and XeLaTeX, then verifies the toolchain and exact fonts before typesetting. Chinese and English PDFs are generated for the languages actually detected.

~~~text
DocumentCatalog → Sphinx LaTeX → XeLaTeX + configured fonts → validated PDFs
~~~

The LaTeX configuration controls covers, contents, headers, page numbers, bookmarks, and chapter breaks. Tables, code blocks, inline code, images, and WebP have dedicated handling. PDF_STYLE supports web, thesis, graduate, and academic layouts.

~~~bash
python utils/pdf_environment.py --no-auto-install
python build_local.py --clean
~~~

Files are placed in source/_build/html/_static. A missing font fails the build rather than silently falling back, preventing local/CI differences in glyphs, page breaks, and code widths.
