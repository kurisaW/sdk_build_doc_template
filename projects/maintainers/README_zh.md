# 维护者指南

模板的维护边界是：内容作者只需要维护 projects，构建器维护者负责 source 中的发现、同步、导航、HTML、PDF、版本和测试模块。任何新功能都应明确它影响的内容清单、语言行为、HTML 输出、PDF 输出和 CI 验证。

## 架构职责

| 模块 | 职责 |
| --- | --- |
| DocumentCatalog | 发现文档和资源，执行路径与分类约束 |
| FileProcessor 与 IndexGenerator | 同步内容，生成语言化导航和目录首页 |
| html_builder | 分别构建语言站点并写入稳定入口 |
| pdf_builder 与 pdf_environment | 验证 PDF 环境，生成并校验文件 |
| build.py 与 build_manager | 解析版本矩阵，隔离 worktree 并汇总产物 |

## 贡献要求

修改发现或导航逻辑时，至少覆盖 recursive_tree、project_catalog、中文、英文、双语和缺失翻译回退。修改 PDF 逻辑时，除单元测试外，应在包含 XeLaTeX 和配置字体的环境中验证生成文件有效。

:::{admonition} 维护者原则
:class: important
不要把某个输出端的临时修复变成另一个输出端的隐患。HTML、PDF、资源和语言识别应优先复用同一份 DocumentCatalog，而不是各自重新扫描文件系统。
:::
