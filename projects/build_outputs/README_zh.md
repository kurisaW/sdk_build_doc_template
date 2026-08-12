# 构建与输出

构建阶段是模板最重要的工程边界：它将内容目录转换为独立语言站点和严格 PDF，同时清理中间同步副本，避免 source 目录成为第二份不可控内容源。

## 本地工作流

| 目标 | 命令 | 适用时机 |
| --- | --- | --- |
| 只检查环境 | python build_local.py --check | 配置变更后或 CI 前 |
| 快速网页验证 | python build_local.py --clean --no-pdf | 日常写作 |
| 本地浏览 | python build_local.py --clean --no-pdf --serve | 链接、导航和视觉检查 |
| 正式交付检查 | python build_local.py --clean | 合并、打标或发布前 |

Web 与 PDF 的具体体验、字体、版式和输出位置见 [本地构建工作流](01_local_build_zh.md) 与 [PDF 交付](02_pdf_delivery_zh.md)。

:::{admonition} 本地与 CI 使用同一事实源
:class: important
不要为网页和 PDF 维护两套目录或两份导航。它们都由同一个 DocumentCatalog 驱动；任何内容或资源问题都应先在本地暴露，再由 CI 复验。
:::
