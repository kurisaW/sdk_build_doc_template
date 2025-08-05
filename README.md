# SDK Documentation Build Template

**English** | [**中文**](./README_zh.md)

## Introduction

This is a GitHub template repository specifically designed for building SDK documentation. It provides a complete automated documentation build system with the following features:

* 🚀 **Automatic Documentation Structure Generation** – Automatically categorizes and generates documentation based on the project directory.
* 📚 **Multi-Version Support** – Enables building and switching between multiple documentation versions.
* 🌐 **Multi-Platform Deployment** – Supports deployment to GitHub Pages and Read the Docs.
* 🎨 **Modern UI** – Beautiful interface built on Sphinx with the Read the Docs theme.
* 🔧 **Easy Configuration** – Quickly customizable via YAML configuration files.

## Directory Structure

```
docs/source/
├── build_manager.py          # Central build manager
├── build.py                  # Simplified build entry point
├── utils/
│   └── version_utils.py     # Version management utilities
├── _build/
│   ├── worktrees/           # Temporary Git worktrees
│   │   ├── v1.0/
│   │   └── latest/
│   ├── versions/            # Final versioned documentation
│   │   ├── v1.0/
│   │   └── latest/
│   └── html/                # Unified access entry
```

## Key Features

### 1. Isolated Builds Based on Git Worktrees

* Creates independent Git worktrees for each version.
* Avoids branch switching in the main working directory.
* Ensures builds are isolated and non-conflicting.

### 2. Fully Dynamic Version Management

* All version information is dynamically read from `.github/versions.json`.
* Add new versions without modifying scripts.
* Supports automatic version discovery and building.

### 3. Simplified Usage

* Unified build command: `python build.py`
* Automatically handles builds for all configured versions.
* Supports local preview and validation.

## Configuration File

### .github/versions.json

```json
{
  "versions": [
    {
      "name": "master",
      "display_name": "Latest Version",
      "branch": "master",
      "url_path": "latest",
      "description": "Latest development version"
    },
    {
      "name": "v1.0",
      "display_name": "v1.0",
      "branch": "v1.0",
      "url_path": "v1.0",
      "description": "Stable release v1.0"
    }
  ],
  "default_version": "master",
  "latest_version": "master"
}
```

## Usage

### Local Build

```bash
# Build all versions
cd docs/source
python build.py

# Clean build directory before building
python build.py --clean

# Build and start local preview server
python build.py --serve

# Validate version configuration
python build.py --validate

# List all available versions
python build.py --list-versions
```

### Adding a New Version

1. Create a new branch: `git checkout -b v2.0`
2. Add the version configuration to `.github/versions.json`:

```json
{
  "name": "v2.0",
  "display_name": "v2.0",
  "branch": "v2.0",
  "url_path": "v2.0",
  "description": "Version 2.0"
}
```

3. Commit the changes: `git commit -am "Add v2.0 version"`
4. Push the branch: `git push origin v2.0`

### GitHub Actions

* Automatically detects changes to `.github/versions.json`
* Dynamically builds all configured versions
* Deploys to GitHub Pages automatically

## Advantages

### 1. Avoids Branch Switching Issues

* Uses Git worktrees to create isolated working directories per version.
* Does not affect the current working branch.
* Enables more stable and reliable builds.

### 2. Fully Dynamic Configuration

* Add new versions by editing `.github/versions.json` only.
* No need to modify any script files.
* Supports any number of versions.

### 3. Better Isolation

* Each version is built independently.
* Avoids version conflicts.
* Supports parallel builds (if resources allow).

### 4. Simplified Maintenance

* Unified build entry point.
* Automated version management.
* Clear error handling and logging.

## Troubleshooting

### Common Issues

1. **Failed to Create Git Worktree**

   * Ensure the branch exists: `git branch -a`
   * Check your Git version: `git --version`

2. **Version Configuration Validation Failed**

   * Verify the format of `.github/versions.json`
   * Ensure all required fields are present
   * Check that the branch exists

3. **Build Failed**

   * Check Python dependencies: `pip install -r requirements.txt`
   * Review detailed error logs
   * Try rebuilding with `--clean` flag

### Debug Commands

```bash
# Validate version configuration
python utils/version_utils.py --validate

# List all versions
python utils/version_utils.py --list

# Get current Git branch
python utils/version_utils.py --current-branch

# Get version info by branch
python utils/version_utils.py --version-for-branch master

# Get branch name by version
python utils/version_utils.py --branch-for-version master
```

## Contribution Guidelines

1. Always run validation before modifying version configurations.
2. Ensure the branch is created and pushed when adding a new version.
3. Test the build process before committing any changes.
4. Keep this documentation up to date with any changes made.
