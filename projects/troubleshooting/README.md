# Troubleshooting

Start by identifying the failing stage. Do not manually delete synchronized files or edit generated navigation under source; the builder tracks them and removes them after a successful build.

| Symptom | Check first | Command |
| --- | --- | --- |
| Missing page or image | Relative path, suffix, and projects boundary | python build_local.py --clean --no-pdf |
| Missing switcher or landing-page fallback | Root README pair and counterpart names | python build_local.py --clean --no-pdf |
| Empty or duplicated category | patterns, entry_files, duplicate_categories | python build.py --validate |
| Missing PDF font or XeLaTeX | config.yaml font names and pdf_environment | python utils/pdf_environment.py --no-auto-install |
| Local and CI differ | Python, requirements, fonts, and locale | Compare workflow installation steps |

Check dependencies without auto-installation, build web output cleanly first, inspect generated pages and assets, then run the full PDF build. Compare the GitHub Actions artifact rather than only a cached Pages site.
