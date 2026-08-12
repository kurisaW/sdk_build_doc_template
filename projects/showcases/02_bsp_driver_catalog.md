# Showcase: BSP and Driver Catalog

A BSP repository may contain evaluation boards, sensor drivers, reference projects, vendor code, and build caches. The public site should show maintained project entry points rather than recursively scanning every README, so choose project_catalog.

~~~yaml
categories:
  boards:
    name: "Boards"
    patterns: ["board_*"]
  drivers:
    name: "Drivers"
    patterns: ["driver_*"]
generation:
  discovery:
    mode: project_catalog
    entry_files:
      zh: README_zh.md
      en: README.md
    asset_globs: ["figures/**", "assets/**"]
    unmatched_projects: error
    duplicate_categories: error
  navigation:
    mode: categories
    order: ["boards", "drivers"]
~~~

Vendor trees, package caches, and fixtures often contain READMEs but are not public support material. The strict catalog publishes only selected project landings and declared assets, then blocks duplicate ownership. A build failure becomes a useful governance signal when a new board is uncategorized, an entry document is missing, or an image was not included.
