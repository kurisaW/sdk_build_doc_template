# 内容创作

高质量文档的可维护性首先来自约定，而不是复杂工具。模板采用目录首页加正文页面的结构：每个章节有一对 README，正文在同目录内按自然排序组织；中文文件使用 _zh 后缀，英文文件使用相同基础名但不带后缀。

## 推荐目录形态

~~~text
projects/
└── authoring/
    ├── README_zh.md
    ├── README.md
    ├── 01_content_conventions_zh.md
    ├── 01_content_conventions.md
    └── figures/
        └── naming-example.png
~~~

目录 README 是章节入口：网页侧栏将其作为可读的章节首页，PDF 将其标题作为大章节标题。不要手工维护 source 中同步出来的副本；每次成功构建后，生成器都会清理这些中间文件。

## 内容表达

Markdown 是默认格式，MyST 提供提示框、任务列表、定义列表、数学公式和更丰富的引用；已有 reStructuredText 内容也可以逐步保留。技术内容应优先回答：读者要达到什么目标、前置条件是什么、执行结果如何验证、失败后去哪里排查。

阅读 [内容约定](01_content_conventions_zh.md) 了解命名和资产规则；双语项目继续阅读 [双语编写](02_bilingual_authoring_zh.md)。
