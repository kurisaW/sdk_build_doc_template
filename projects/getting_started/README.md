# Quick Start

The goal is not merely to run a command. This route verifies content discovery, language detection, HTML output, and the publishing entry point in the shortest possible path. Start without PDFs, then prepare XeLaTeX once the web flow is correct.

~~~powershell
git clone https://github.com/your-org/your-docs.git
cd your-docs
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
cd source
python build_local.py --check
python build_local.py --clean --no-pdf --serve
~~~

Open http://localhost:8000. See [First Local Build](01_first_build.md) for outputs and command options. HTML only needs Python dependencies; PDF generation also requires XeLaTeX and exact fonts, so use --no-pdf during daily authoring and run the full build before release.
