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

## Web 布局与响应式行为

页面使用左侧全局目录、中间正文和右侧文章大纲。正文宽度在 680px 到 960px 之间连续变化，右侧大纲保持约 220px 到 280px；布局根据 .wy-nav-content 的实际容器宽度判断是否堆叠，而不是依赖单一视口断点。窄屏时大纲移动到正文下方，避免横向滚动和无意义的空白。

文章大纲只读取当前正文的 h2/h3，使用纯文本标签并保留嵌套层级。点击后平滑滚动，IntersectionObserver 根据阅读位置更新高亮；左侧导航状态由 navigation_state.js 保存，跨页面后仍恢复之前的展开路径。

:::{admonition} 本地与 CI 使用同一事实源
:class: important
不要为网页和 PDF 维护两套目录或两份导航。它们都由同一个 DocumentCatalog 驱动；任何内容或资源问题都应先在本地暴露，再由 CI 复验。
:::
