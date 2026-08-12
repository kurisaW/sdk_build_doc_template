# Authoring

Maintainable documentation starts with conventions rather than complicated tooling. Each section has a README pair as its landing page; body pages live beside it and use natural ordering. Chinese files use the _zh suffix, while English counterparts use the same base name without it.

~~~text
projects/
└── authoring/
    ├── README_zh.md
    ├── README.md
    ├── 01_content_conventions_zh.md
    └── 01_content_conventions.md
~~~

The directory README is both a readable web landing page and a PDF chapter boundary. Do not edit synchronized copies under source. Markdown is the default format; MyST adds admonitions, task lists, definition lists, math, and richer references, while existing reStructuredText can remain in place. Read [Content Conventions](01_content_conventions.md) and [Bilingual Authoring](02_bilingual_authoring.md).
