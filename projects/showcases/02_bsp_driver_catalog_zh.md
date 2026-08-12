# 示例：BSP 与驱动项目目录

## 场景

一个 BSP 仓库包含评估板、传感器驱动、参考工程、供应商代码和构建缓存。公开站点应展示经过维护的项目入口，而不是递归扫描所有 README，因此选择 project_catalog。

~~~yaml
categories:
  boards:
    name: "开发板"
    patterns: ["board_*"]
  drivers:
    name: "驱动"
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

## 为什么这比递归扫描更可靠

供应商目录、包管理缓存和测试夹具经常包含 README，但它们并不属于公开支持范围。严格项目目录只发布分类规则选中的项目入口和图像资源，并阻止一个项目同时归属多个分类。

构建失败本身就是治理信号：新增加的板卡如果没有对应分类、项目没有入口 README，或 README 引用了未收录图片，CI 会直接指出问题。
