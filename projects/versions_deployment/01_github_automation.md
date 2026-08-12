# GitHub Actions and GitHub Pages Release Automation

The bundled workflow watches source, projects, and versions.json. It separates valid configuration, usable PDF tooling, buildable versions, and deployable artifacts instead of discovering errors only at the final step.

| Job or step | Responsibility | Result |
| --- | --- | --- |
| validate-versions | Install Python 3.11, dependencies, and run build.py --validate | Invalid version configuration is blocked |
| build-docs | Install XeLaTeX, fonts, and locale; verify PDF tooling | HTML and PDF are built for every version |
| upload-artifact | Upload source/source_build/html | Pull requests have a downloadable review artifact |
| deploy-docs | On main or master only, publish the artifact | GitHub Pages is updated on an orphan branch |

Pull requests validate and build but do not deploy. After merge, peaceiris/actions-gh-pages publishes the identical artifact with force_orphan. Before release, validate versions, inspect deep links and assets locally, run a complete PDF build in a matching environment, test both language routes, and confirm the artifact matches the Pages entry.
