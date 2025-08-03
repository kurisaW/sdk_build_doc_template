# SDK Documentation Build Template

**English** | [**中文**](./README_zh.md)

## Introduction

This is a GitHub template repository designed specifically for building SDK documentation. It provides a complete set of automated documentation build mechanisms, including:

* 🚀 **Automatic Documentation Structure Generation** – Automatically categorizes and generates documentation based on the project directory
* 📚 **Multi-Version Support** – Supports building and switching between multiple versions of documentation
* 🌐 **Multi-Platform Deployment** – Compatible with GitHub Pages and Read the Docs
* 🎨 **Modern Interface** – Beautiful UI based on Sphinx and the Read the Docs theme
* 🔧 **Easy Configuration** – Quickly customizable via a YAML configuration file

## Directory Structure

```
sdk-docs-template/
├── source/                    # Core documentation build directory
│   ├── conf.py               # Sphinx configuration file
│   ├── config.yaml           # Project configuration file
│   ├── build_local.py        # Local build script
│   ├── doc_generator.py      # Documentation generator
│   ├── version_generator.py  # Version generator
│   ├── setup_new_project.py  # New project setup script
│   ├── requirements.txt      # Python dependencies
│   └── _static/              # Static assets
├── projects/                 # Example projects directory
│   ├── basic_example/        # Basic example
│   ├── driver_example/       # Driver example
│   └── component_example/    # Component example
├── .github/workflows/        # GitHub Actions workflows
├── .readthedocs.yaml         # Read the Docs configuration
└── README.md                 # Project description
```

## Quick Start

### 1. Create a New Repository Using the Template

1. Click the "Use this template" button
2. Select "Create a new repository"
3. Fill in the repository name and description
4. Click "Create repository from template"

### 2. Configure the Project

```bash
# Enter the source directory
cd source

# Run the project setup script
python setup_new_project.py
```

Follow the prompts to fill in the project information. The script will generate the configuration file automatically.

### 3. Build the Documentation

```bash
# Check dependencies
python build_local.py --check

# Build documentation
python build_local.py

# Preview locally
python build_local.py --serve
```

### 4. Deploy the Documentation

#### GitHub Pages (Recommended)

Push to the `master` or `main` branch, and GitHub Actions will automatically build and deploy to GitHub Pages.

#### Read the Docs

1. Connect your repository on Read the Docs
2. Select `source/conf.py` as the configuration file
3. The build will start automatically

## Configuration Guide

### Project Configuration (`config.yaml`)

```yaml
project:
  name: "Your_SDK_Docs"
  title: "Your SDK Documentation"
  description: "SDK documentation description"
  version: "1.0.0"
  author: "Your Name"
  copyright: "2025, Your Company"

categories:
  basic:
    name: "Basics"
    description: "Basic feature examples"
    patterns:
      - "basic_*"
  
  driver:
    name: "Drivers"
    description: "Peripheral driver examples"
    patterns:
      - "driver_*"
```

### Documentation Categories

The system supports the following documentation categories:

* **Basics** – Basic feature examples
* **Drivers** – Peripheral driver examples
* **Components** – Network component examples
* **Protocols** – Industrial protocol examples

### Project Naming Convention

The documentation generator automatically categorizes projects based on name patterns:

* `basic_*` → Basics
* `driver_*` → Drivers
* `component_*` → Components
* `protocol_*` → Protocols

## Features

### 🔄 Automated Documentation Generation

* Scans project directories automatically
* Categorizes based on naming rules
* Generates a unified documentation structure
* Supports both Markdown and RST formats

### 📋 Multi-Version Management

* Supports multiple branch versions
* Automatically generates a version switcher menu
* Isolated documentation per version

### 🎨 Modern Interface

* Responsive design
* Light/Dark themes
* Built-in search
* Mobile-friendly layout

### ⚡ Fast Builds

* Incremental builds
* Parallel processing
* Caching mechanism
* Local preview support

## Developer Guide

### Adding a New Project

1. Create a new project under the `projects/` directory
2. Name the project according to the naming convention
3. Add a `README.md` file
4. Run the build script

### Customizing the Theme

Modify the theme configuration in `source/conf.py`:

```python
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'titles_only': False,
}
```

### Adding Custom CSS/JS

Add static files to the `source/_static/` directory and reference them in `conf.py`:

```python
html_css_files = ['custom.css']
html_js_files = ['custom.js']
```

## Troubleshooting

### Common Issues

**Q: What if the build fails?**
A: Check whether Python dependencies are correctly installed. Run `pip install -r requirements.txt`

**Q: Why aren’t the documents automatically categorized?**
A: Check if project names follow the correct pattern, or adjust the pattern in `config.yaml`

**Q: GitHub Pages deployment failed?**
A: Verify if `.github/workflows/gh-pages.yml` is properly configured

### Debug Mode

```bash
# Verbose output
python build_local.py --verbose

# Clean build
python build_local.py --clean

# Check branch versions
python build_local.py --check-branch
```

## Contribution Guide

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 – See the [LICENSE](LICENSE) file for details.

## Support

If you encounter issues while using the project:

1. Check the [Issues](../../issues) page
2. Create a new issue describing the problem
3. Provide detailed error information and reproduction steps

---

**Make SDK documentation building simple and efficient!** 🚀
