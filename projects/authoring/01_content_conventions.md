# Content Conventions for Long-Lived Documentation

| Content type | Chinese | English |
| --- | --- | --- |
| Site or section landing page | README_zh.md | README.md |
| Markdown body page | topic_zh.md | topic.md |
| reStructuredText body page | topic_zh.rst | topic.rst |
| Images and attachments | figures/ or assets/ | Shared in the same directory |

Place counterpart documents in the same directory and keep the same base name, such as install_zh.md and install.md. Use stable English snake_case paths; put reader-facing language in the document title and category display name.

Every technical page should state its goal and applicable version, prerequisites, runnable steps and execution environment, a success criterion, and a link for likely failures. Keep images next to their article and reference them relatively. The builder validates that local images exist and stay inside projects, so do not rely on escaping ../ paths.
