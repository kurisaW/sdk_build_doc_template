# 选择递归文档树还是严格项目目录

## 选择 recursive_tree

当文档目录本身就是读者的学习路线时，使用 recursive_tree。它递归同步 Markdown、RST 与图片，并使用目录 README 作为章节首页。适用于安装指南、API 手册、产品教程和架构知识库。

~~~text
projects/
├── getting_started/
│   ├── README_zh.md
│   └── install_zh.md
└── reference/
    ├── README_zh.md
    └── configuration_zh.md
~~~

## 选择 project_catalog

当仓库同时含有源码、供应商包、构建输出和多个独立示例时，使用 project_catalog。通过 categories.*.patterns 选择项目根目录，仅收录 entry_files 和 asset_globs 声明的文件。

~~~text
projects/
├── board_alpha/
│   ├── README_zh.md
│   ├── README.md
│   └── figures/
└── vendor/
    └── third_party_library/
~~~

严格模式会拒绝空匹配、重复分类、缺少项目入口 README、越界路径和未同步图片。它的价值在于明确地证明“发布了什么”和“没有发布什么”。

:::{admonition} 不要混合职责
:class: warning
不要用目录命名技巧模拟项目白名单，也不要用分类模式代替一本连续手册的章节层级。先选择发现模型，再配置导航，文档结构会更易维护。
:::
