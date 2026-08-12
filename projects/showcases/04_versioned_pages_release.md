# Showcase: Versioned GitHub Pages Release

An open-source SDK may evolve on main while users still need the installation commands and APIs for v1.1. Publish latest and stable branches together so new readers see current capability without breaking historical users.

Declare main and v1.1 in versions.json, then set main as both default_version and latest_version. The builder creates a separate worktree for every branch instead of checking out the current directory. Pull requests produce artifacts for review; after merge, the deployment job publishes the identical artifact to GitHub Pages. The version menu reads the generated version description, so static links do not need manual maintenance.
