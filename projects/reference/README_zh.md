# 配置参考

本章用于查找准确字段和命令，不重复解释工作流。新项目可从 source/config_templates 中选择 recursive_tree.yaml 或 project_catalog.yaml，再替换项目元数据、目录和分类。

## 高频配置

| 字段 | 用途 |
| --- | --- |
| repository.projects_dir | 相对 source/config.yaml 的内容根目录 |
| generation.discovery.mode | recursive_tree 或 project_catalog |
| generation.navigation.order | 顶层分类或目录显示顺序 |
| generation.navigation.maxdepth | 全局目录深度；-1 表示保留完整目录树 |
| generation.navigation.titles_only | 全局目录是否只显示文档和目录标题 |
| generation.navigation.show_local_toc | 是否在文章右侧生成 h2/h3 大纲 |
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

## 页面相关实现

| 文件 | 作用 |
| --- | --- |
| source/_templates/layout.html | 输出左侧全局树、正文容器和右侧大纲挂载点 |
| source/_static/custom.css | 控制三栏宽度、容器查询、层级缩进和窄屏堆叠 |
| source/_static/page_outline.js | 从当前正文提取 h2/h3，生成纯文本嵌套大纲并更新阅读高亮 |
| source/_static/navigation_state.js | 维护唯一展开路径和页面/锚点跳转后的导航状态 |
