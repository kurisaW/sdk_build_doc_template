# Bilingual Authoring and Language Switching

Bilingual documentation is not two languages mixed on one page. The template builds Chinese and English source files independently, with separate navigation, search indexes, and static assets. The switcher appears only when both root README markers are present.

| Current page | Counterpart exists | Counterpart missing |
| --- | --- | --- |
| setup_zh.md | Opens setup.md | Opens the English landing page |
| setup.md | Opens setup_zh.md | Opens the Chinese landing page |

This fallback supports incremental translation without a broken switcher. Add a counterpart with the same base name when it is ready; no frontend logic needs to change. Keep APIs, commands, paths, configuration fields, and values unchanged, but rewrite explanatory prose for the target reader rather than translating word by word.
