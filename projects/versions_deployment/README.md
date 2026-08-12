# Versions and Deployment

A documentation version is not a display label. It is a reproducible source snapshot. The template declares version entry points in .github/versions.json, builds every branch in an isolated Git worktree, and lets GitHub Actions apply the same release rules to pull requests and the default branch.

~~~text
versions.json → validate → isolated Git worktrees → build every version → HTML/PDF artifacts → GitHub Pages
~~~

| Goal | Entry point |
| --- | --- |
| Validate definitions | python build.py --validate |
| Inspect the matrix | python build.py --list-versions |
| Build all versions | python build.py --clean |
| Check the current branch | python build_local.py --check-branch |

See [GitHub Release Automation](01_github_automation.md) for jobs, artifacts, and deployment conditions. Treat the default branch as latest, declare supported stable branches explicitly, validate pull requests first, and deploy only main or master.
