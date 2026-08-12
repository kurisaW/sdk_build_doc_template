# 配置参考

本章用于查找准确字段和命令，不重复解释工作流。新项目可从 source/config_templates 中选择 recursive_tree.yaml 或 project_catalog.yaml，再替换项目元数据、目录和分类。

## 高频配置

| 字段 | 用途 |
| --- | --- |
| repository.projects_dir | 相对 source/config.yaml 的内容根目录 |
| generation.discovery.mode | recursive_tree 或 project_catalog |
| generation.navigation.order | 顶层分类或目录显示顺序 |
| generation.default_page | 各语言网站首页 |
| generation.directory_index | 每个章节目录的首页文件 |
| generation.pdf_style | web、thesis、graduate 或 academic |
| generation.pdf_fonts | 本地和 CI 必须具备的精确字体 |

## 常用命令

| 命令 | 目的 |
| --- | --- |
| python build_local.py --check | 检查本地构建环境 |
| python build_local.py --clean --no-pdf | 快速生成网页 |
| python build.py --validate | 校验 versions.json |
| python build.py --list-versions | 列出版本配置 |
| python build.py --clean | 构建全部版本 |

配置字段的行为说明见 [内容组织](../content_models/README_zh.md)、[构建与输出](../build_outputs/README_zh.md) 和 [版本与部署](../versions_deployment/README_zh.md)。
