# SDK Documentation Build Template

**从目录化 Markdown 到多版本文档站与严格排版 PDF，一套配置完成本地预览和 GitHub Pages 发布。**

[![Build Documentation](https://github.com/kurisaW/sdk_build_doc_template/actions/workflows/build-docs.yml/badge.svg?branch=main)](https://github.com/kurisaW/sdk_build_doc_template/actions/workflows/build-docs.yml)
![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Sphinx 8.1.3](https://img.shields.io/badge/Sphinx-8.1.3-0A507A?logo=sphinx&logoColor=white)
![MyST 4.0.1](https://img.shields.io/badge/MyST-4.0.1-2C4F7C)
![PDF XeLaTeX](https://img.shields.io/badge/PDF-XeLaTeX-008080)
![Docs Chinese and English](https://img.shields.io/badge/Docs-%E4%B8%AD%E6%96%87%20%7C%20English-5C6AC4)
[![Use this template](https://img.shields.io/badge/Use_this_template-2EA44F?logo=github&logoColor=white)](https://github.com/kurisaW/sdk_build_doc_template/generate)

[English](./README.md) · **简体中文**

本仓库面向 SDK、硬件平台、机器人系统和工程软件等开发者文档场景。文档作者只维护 `projects/` 中的 Markdown、reStructuredText 与图片资源；构建系统负责发现语言、生成导航、隔离构建中英文页面、排版 PDF、管理版本并发布静态站点。

它不是简单的 Markdown 转 HTML 脚本。仓库把内容组织、网站信息架构、双语路由、PDF 字体和 CI 环境都纳入同一套可验证的构建约束，使本地预览与远端输出保持一致。

<p>
  <a href="#readme-quick-start">快速开始</a> ·
  <a href="#readme-core-design">核心设计</a> ·
  <a href="#readme-content-model">内容模型</a> ·
  <a href="#readme-configuration">配置</a> ·
  <a href="#readme-pdf">PDF</a> ·
  <a href="#readme-versions">多版本</a> ·
  <a href="#readme-troubleshooting">故障排查</a>
</p>

<a id="readme-core-design"></a>
## 核心设计

| 设计目标 | 当前机制 |
| --- | --- |
| 内容与工具解耦 | `projects/` 保存文档源，`source/` 保存构建系统；同步副本由清单管理 |
| 两种内容模型 | 文档树保留目录层级与目录 README；项目目录只收录项目入口 README 与声明资源 |
| 全链路目录一致 | 文件同步、语言识别、HTML 导航与 PDF 扫描共享同一份 `DocumentCatalog` |
| 双语按需启用 | 自动识别仅中文、仅英文或中英文；只有双语站点显示切换控件 |
| 构建结果可复现 | Python 依赖锁定版本，PDF 严格校验 XeLaTeX 与精确字体，不允许静默回退 |
| 本地与 CI 同构 | 本地和 GitHub Actions 使用相同配置、字体角色与 PDF 生成路径 |
| 版本互不干扰 | 多版本构建为每个 Git 分支创建独立 worktree，不切换当前工作目录 |

### 输出能力

- 基于 Sphinx 8 和 Read the Docs Theme 的静态文档站。
- 基于 MyST Parser 的 Markdown、表格、数学公式、任务列表和扩展语法。
- 中英文独立搜索索引、静态资源与准确的对应页跳转。
- XeLaTeX 生成的中英文 PDF，包含封面、目录、页码、书签和章节换页。
- 对代码块、行内代码、表格、链接、图片及 WebP 的统一 PDF 排版。
- `.github/versions.json` 驱动的多版本入口与 GitHub Pages 发布。
- 可选的 giscus 评论、编辑入口、暗色样式、版本菜单和 PDF 下载入口。

<a id="readme-quick-start"></a>
## 快速开始

### 环境要求

| 场景 | 必需环境 |
| --- | --- |
| HTML 构建 | Python 3.11 推荐；Python 依赖可由脚本自动安装 |
| PDF 构建 | XeLaTeX，以及 `source/config.yaml` 中声明的全部字体 |
| 多版本构建 | Git 和 `.github/versions.json` 中可访问的目标分支 |

### 1. 创建本地环境

```bash
git clone https://github.com/kurisaW/sdk_build_doc_template.git
cd sdk_build_doc_template
python -m venv .venv
```

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
cd source
python build_local.py --check
```

```bash
# Linux/macOS
source .venv/bin/activate
cd source
python build_local.py --check
```

`--check` 会校验 `requirements.txt` 中的依赖及精确版本。缺失时默认自动安装；使用 `--no-auto-install` 可切换为只检查模式。

### 2. 写入项目文档

```text
projects/
`-- getting_started/
    |-- README_zh.md
    |-- README.md
    |-- install_zh.md
    |-- install.md
    `-- figures/
        `-- installation.png
```

中文文档使用 `_zh` 后缀，英文文档使用相同基础文件名但不带 `_zh`。修改 `source/config.yaml` 中的项目名称、章节和排序后即可构建。

### 3. 构建并预览

```bash
cd source
python build_local.py --clean --serve
```

浏览器访问 `http://localhost:8000`。最终产物位于：

```text
source/_build/html/index.html
source/_build/html/_static/<project.name>.pdf
source/_build/html/_static/<project.name>_EN.pdf   # 检测到英文时生成
```

日常只检查网页内容时可以跳过 PDF，以缩短构建时间：

```bash
python build_local.py --clean --no-pdf --serve
```

## 构建机制

```text
projects/ + repository README
                |
                v
        language detection
                |
                v
        doc_generator.py
   sync sources + create navigation
                |
        +-------+-------+
        |               |
        v               v
  Sphinx HTML      Sphinx LaTeX
  zh/en isolated       + XeLaTeX
        |               |
        +-------+-------+
                v
       source/_build/html/
```

一次本地构建依次执行：

1. 检查锁定的 Python 依赖，必要时选择可用软件源安装。
2. 将 `projects/` 中允许的文档与资源同步到 Sphinx source。
3. 按共享文档目录清单同步源文件，并根据配置生成各语言导航。
4. 分别构建中文和英文 HTML，再合并为统一站点。
5. 按实际语言生成一份或两份 PDF，并验证文件有效性。
6. 删除同步副本、LaTeX、doctree 和构建元数据，保留最终 HTML/PDF。

<a id="readme-content-model"></a>
## 内容模型

### 文档源与仓库结构

```text
.
|-- projects/                         # 唯一主要文档源
|   |-- README_zh.md                  # 可选：projects 中文首页/语言标记
|   |-- README.md                     # 可选：projects 英文首页/语言标记
|   `-- <section>/
|       |-- README_zh.md              # 可选：中文目录首页
|       |-- README.md                 # 可选：英文目录首页
|       |-- <topic>_zh.md             # 中文正文
|       |-- <topic>.md                # 英文正文
|       `-- figures/                  # 图片资源
|-- source/
|   |-- build_local.py                # 本地单版本入口
|   |-- build.py                      # 多版本入口
|   |-- build_manager.py              # worktree 与版本编排
|   |-- doc_generator.py              # 同步与导航生成
|   |-- config.yaml                   # 项目配置
|   |-- conf.py                       # Sphinx 与 LaTeX 配置
|   |-- requirements.txt              # 锁定依赖
|   |-- tests/                        # 机制测试
|   |-- utils/                        # 构建模块
|   |-- _static/                      # 网站资源
|   `-- _templates/                   # 页面模板
|-- .github/versions.json             # 多版本定义
|-- .github/workflows/build-docs.yml  # CI 与 Pages 发布
|-- README_zh.md                      # 中文仓库说明/首页回退
`-- README.md                         # 英文仓库说明/首页回退
```

`projects/` 是内容事实源。不要手工编辑构建时出现在 `source/` 下的同名目录或 README；这些文件由 `.doc_generator_manifest.json` 记录并自动清理。

### 语言命名

| 文档类型 | 中文 | 英文 |
| --- | --- | --- |
| 网站或目录首页 | `README_zh.md` | `README.md` |
| Markdown 正文 | `<name>_zh.md` | `<name>.md` |
| reStructuredText 正文 | `<name>_zh.rst` | `<name>.rst` |

对应页面应位于同一目录并保持相同基础文件名。例如 `install_zh.md` 对应 `install.md`。双语站点中，目标语言页面不存在时，切换器会跳转到该语言首页。

### 语言识别优先级

`generation.language_detection` 默认使用 `README_zh.md` 和 `README.md` 作为语言标记。`recursive_tree` 模式遵循以下优先级：

1. `projects/` 根目录存在任一语言标记时，根目录标记具有最高优先级，并完整决定可用语言。
2. `projects/` 根目录没有任何标记时，合并检查仓库根 README 和各文档目录 README。
3. 只检测到一种语言时仅构建该语言，不显示切换控件。
4. 同时检测到中文和英文时构建双语站点并显示切换控件。
5. 没有任何标记时，PDF 构建停止并报告无法识别语言。

因此，仅存在 `projects/README_zh.md` 时，子目录里的英文 README 不会额外启用英文站点。这可以防止少量未完成翻译误触发全站双语入口。

`project_catalog` 模式只统计分类规则选中的项目入口 README，以及 `projects_dir` 或仓库根的首页 README。项目可以只提供一种语言；只要最终目录清单同时包含中英文入口，站点就会生成双语版本并显示切换控件。供应商包、板级源码和其他未选中的嵌套 README 不参与语言判断。

### 网站首页优先级

每种语言独立选择首页：

```text
generation.default_page
          |
          | missing
          v
repository-root README fallback
          |
          | missing
          v
generated language index
```

- `generation.default_page` 相对于 `repository.projects_dir`，不得使用绝对路径或 `..`。
- 只有 `projects/` 根目录完全没有语言 README 时，才启用仓库根 README 回退。
- 仓库根 README 只会被复制到受清单管理的临时位置，源文件不会被修改。
- 构建器会解析回退 README 中的 Markdown、MyST、RST 和 HTML 图片引用，精确同步对应本地图片并保持相对 URL；缺图或路径越界会直接终止构建。

### 两种发现与导航模式

文档收录范围和导航结构是两个独立维度：

| 场景 | `generation.discovery.mode` | `generation.navigation.mode` | 行为 |
| --- | --- | --- | --- |
| 教程、手册、知识库 | `recursive_tree` | `directory_tree` | 递归同步受支持的文档和资源，以目录 README 作为章节首页 |
| SDK/BSP 示例集合 | `project_catalog` | `categories` | 只同步分类规则选中的项目根 README 与 `asset_globs` 资源，按分类生成导航 |

`project_catalog` 中，不含 `/` 的 `categories.*.patterns` 只匹配 `projects_dir` 的一级目录；嵌套项目必须写出完整相对路径，例如 `dual_core/core0`。同一项目匹配多个分类、模式匹配为空、项目没有任一入口 README、导航顺序引用未知分类、路径越界或 README 图片未被同步时，构建会直接失败。

HTML、语言识别、文件同步和 PDF 都使用同一个 `DocumentCatalog`，因此不会再出现网站只展示项目首页、PDF 却递归收录第三方包 README 的差异。

### 每个目录一个 README

每个目录、每种语言按以下顺序选择章节首页：

1. `generation.directory_index` 配置的 README。
2. 已存在的 `index_zh.rst` / `index.rst` 或对应 Markdown 索引。
3. 构建器自动生成的语言索引。

该规则仅适用于 `recursive_tree`。目录 README 可以包含章节简介，也可以只保留一级标题。构建器只向临时副本追加隐藏 `toctree`。生成 PDF 时，导航 README 保留一级标题作为章节标题，但正文不进入 PDF；如果目录中只有 README，则将其作为独立正文处理。`project_catalog` 的项目根 README 是项目正文，PDF 会保留项目标题并收录其正文。

### 排序与标题

- 顶层章节优先按 `generation.navigation.order` 排序，未列出的已配置分类自然追加；`generation.output_structure` 仅作为旧配置兼容键。
- 目录内文档按路径自然排序，可使用 `01_`、`02_` 文件名前缀稳定顺序。
- `categories.<path>.name` 和 `name_en` 控制生成页及 PDF 的章节显示名称。
- 每篇文章建议只保留一个一级标题，不手工重复文件名前缀中的序号。
- PDF 构建只对 LaTeX 输出剥离常见手工标题编号，HTML 和源文件保持原样。

<a id="readme-configuration"></a>
## 配置

可直接从 [`source/config_templates/`](source/config_templates/README_zh.md) 选择完整模板：文档型仓库使用 `recursive_tree.yaml`，SDK/BSP 示例集合使用 `project_catalog.yaml`。

以下配置覆盖目录树、双语首页、章节排序和严格 PDF 字体：

```yaml
project:
  name: "Example_SDK"
  title: "Example SDK 开发文档"
  title_en: "Example SDK Documentation"
  description: "Example SDK 的开发、集成与调试文档。"
  description_en: "Development, integration, and debugging documentation for Example SDK."
  version: "1.0.0"
  author: "Example Team"
  copyright: "2026, Example Team"
  website: "https://example.com"

repository:
  name: "example-sdk-docs"
  projects_dir: "../projects"
  docs_dir: "."

categories:
  getting_started:
    name: "快速上手篇"
    name_en: "Getting Started"
    description: "环境准备和首个示例。"
    description_en: "Environment setup and first example."
  applications:
    name: "应用篇"
    name_en: "Applications"

generation:
  mode: "directory_tree"
  discovery:
    mode: "recursive_tree"
  navigation:
    mode: "directory_tree"
    order:
      - "getting_started"
      - "applications"
  language_detection:
    zh: "README_zh.md"
    en: "README.md"
  default_language: "zh"
  default_page:
    zh: "README_zh.md"
    en: "README.md"
  directory_index:
    zh: "README_zh.md"
    en: "README.md"
  sync_extensions:
    - ".md"
    - ".rst"
    - ".png"
    - ".jpg"
    - ".jpeg"
    - ".gif"
    - ".svg"
    - ".webp"
  pdf_style: "web"
  pdf_fonts:
    latin: "TeX Gyre Termes"
    cjk_body: "FandolSong-Regular.otf"
    cjk_heading: "FandolHei-Regular.otf"
    cjk_emphasis: "FandolKai-Regular.otf"
    code: "Source Code Pro"

sphinx:
  theme: "sphinx_rtd_theme"
  extensions:
    - "myst_parser"
  source_suffix:
    ".rst": "restructuredtext"
    ".md": "markdown"

giscus:
  enabled: false
```

| 配置项 | 作用 |
| --- | --- |
| `project.name` | 项目标识、PDF 文件名和默认 PDF 封面主标题 |
| `project.title` | HTML 站点显示标题 |
| `project.title_en` | 自动生成英文首页时使用的可选标题 |
| `project.description` / `description_en` | 自动首页说明及中英文 PDF 封面摘要 |
| `repository.projects_dir` | 文档源目录，相对于 `source/config.yaml` |
| `repository.docs_dir` | Sphinx source 目录，通常保持 `.` |
| `generation.discovery.mode` | `recursive_tree` 递归文档树，或 `project_catalog` 严格项目目录 |
| `generation.navigation.mode` | `directory_tree` 按目录组织，或 `categories` 按分类组织 |
| `generation.navigation.order` | 顶层目录或分类的优先顺序 |
| `generation.default_language` | 首选语言；不可用时选择实际检测到的语言 |
| `generation.default_page` | 各语言网站首页，相对于 `projects_dir` |
| `generation.directory_index` | 各语言目录首页文件名 |
| `generation.sync_extensions` | 允许同步的文档和资源扩展名 |
| `generation.pdf_style` | `web` 为默认；`thesis` / `graduate` / `academic` 启用论文预览参数 |
| `generation.pdf_fonts` | PDF 各文本角色使用的精确字体 |
| `giscus.enabled` | 是否加载 giscus；启用后还需填写仓库与分类标识 |

SDK/BSP 示例集合可改用严格项目目录模式：

```yaml
categories:
  basic:
    name: "基础篇"
    name_en: "Basics"
    patterns:
      - "Titan_basic_*"
  multicore:
    name: "多核通信篇"
    name_en: "Multicore Communication"
    patterns:
      - "Titan_dual_core/Titan_dual_core0"
      - "Titan_dual_core/Titan_dual_core1"

generation:
  mode: "project_catalog"          # 兼容旧脚本的模式标记
  discovery:
    mode: "project_catalog"
    entry_files:
      zh: "README_zh.md"
      en: "README.md"
    asset_globs:
      - "figures/**"
    unmatched_projects: "error"
    duplicate_categories: "error"
  navigation:
    mode: "categories"
    order:
      - "basic"
      - "multicore"
```

## 本地构建

以下命令均在 `source/` 目录执行：

| 命令 | 用途 |
| --- | --- |
| `python build_local.py` | 构建当前工作区的 HTML 与 PDF |
| `python build_local.py --clean` | 删除旧 HTML 后完整重建 |
| `python build_local.py --serve` | 构建后启动本地静态服务器 |
| `python build_local.py --serve --port 8080` | 使用指定端口预览 |
| `python build_local.py --no-pdf` | 只构建 HTML |
| `python build_local.py --check` | 检查并按需安装 Python 依赖 |
| `python build_local.py --check --no-auto-install` | 只检查依赖，不安装 |
| `python build_local.py --check-branch` | 检查当前分支与版本配置映射 |

### 依赖与镜像

自动安装会并发探测 PyPI、清华大学镜像和阿里云镜像，按可达性与延迟排序。已有 `PIP_INDEX_URL` 时优先尝试该地址，再使用探测出的备用源。

```powershell
# Windows PowerShell
$env:DOCS_PIP_MIRROR = "tsinghua"  # auto | official | china | tsinghua | aliyun
python build_local.py --check

$env:DOCS_PIP_INDEX_URL = "https://your-mirror.example/simple/"
python build_local.py --check
```

```bash
# Linux/macOS
DOCS_PIP_MIRROR=official python build_local.py --check
DOCS_PIP_INDEX_URL=https://your-mirror.example/simple/ python build_local.py --check
```

<a id="readme-pdf"></a>
## PDF 构建

PDF 只使用 `Sphinx LaTeX -> XeLaTeX` 路线。失败时不会改用浏览器打印或其他后备引擎，从而避免本地和 CI 得到不同版式。

### 默认字体

| 文本角色 | 字体 |
| --- | --- |
| 英文、数字和西文正文 | TeX Gyre Termes |
| 中文正文 | FandolSong-Regular.otf |
| 中文标题 | FandolHei-Regular.otf |
| 中文强调 | FandolKai-Regular.otf |
| 代码块 | Source Code Pro |

单独验证工具链：

```bash
cd source
python utils/pdf_environment.py --no-auto-install
```

本地脚本可以尝试安装系统依赖：Linux 使用 `apt-get`，macOS 使用 Homebrew，Windows 使用 Chocolatey。该过程取决于系统权限和包管理器；无法自动安装时，需要手工安装 TeX Live 或 MiKTeX，并确保 `xelatex` 位于 `PATH` 或受支持的标准路径。

PDF 排版规则：

- 中英文按检测结果分别生成，英文文件名增加 `_EN`。
- 封面与目录分页，所有页面保留居中页码，正文显示项目名页眉。
- 顶层目录形成一级书签，普通文章形成二级书签，正文目录保留到三级标题。
- 每篇普通文章换页，目录 README 只保留标题，不混入导航正文。
- 正文首行缩进、页边距、段距、标题间距和列表间距由统一 LaTeX 配置控制。
- 表格按版心自动换行；代码块使用等宽字体、浅色背景和可控长行换行。
- 行内代码沿用正文大小，英文和数字使用正文西文字体，不以突兀字号区分。
- WebP 在 LaTeX 阶段转换为 JPEG，避免 XeLaTeX 图像兼容问题。

字体名称必须与 `config.yaml` 完全一致。任一字体不可用时构建直接失败，不允许用“看起来相近”的字体替代。

<a id="readme-versions"></a>
## 多版本与 GitHub Pages

`.github/versions.json` 是版本事实源：

```json
{
  "versions": [
    {
      "name": "main",
      "display_name": "latest",
      "branch": "main",
      "url_path": "latest",
      "description": "最新开发版本"
    },
    {
      "name": "v1.0",
      "display_name": "v1.0",
      "branch": "v1.0",
      "url_path": "v1.0",
      "description": "1.0 稳定版本"
    }
  ],
  "default_version": "main",
  "latest_version": "main"
}
```

每个版本必须包含 `name`、`display_name`、`branch` 和 `url_path`。版本维护命令：

```bash
cd source
python build.py --validate
python build.py --list-versions
python build.py --clean
```

`build.py` 使用 Git worktree 隔离各分支，输出到 `source/source_build/html/`。日常本地预览仍应使用 `build_local.py`，避免不必要的全版本构建。

GitHub Actions 在 Python 3.11/Ubuntu 上完成版本校验、依赖安装、XeLaTeX 与字体校验、多版本构建、产物上传和 `gh-pages` 发布。工作流监听 `source/**`、`projects/**` 和 `.github/versions.json`，也可以通过 `workflow_dispatch` 手动执行。

## 清理策略

`python build_local.py --clean` 会清理旧输出后重新构建，但不会删除源文档：

| 保留 | 自动删除 |
| --- | --- |
| `projects/` 全部源文件 | `source/` 下由清单记录的同步副本 |
| 仓库根 README | `source/_build/latex/` |
| `source/_build/html/` 最终站点 | `source/_build/html/.doctrees/` |
| `source/_build/html/_static/*.pdf` | `source/_build/html/.buildinfo` |
| 构建脚本、配置、模板和静态资源 | 同步后形成的空目录和生成清单 |

构建失败时可能保留中间文件以便排查；修复后重新执行 `python build_local.py --clean`。

<a id="readme-troubleshooting"></a>
## 故障排查

| 现象 | 检查项 |
| --- | --- |
| 未检测到可生成 PDF 的语言 | 确认 `projects/`、文档目录或仓库根存在配置的 README 语言标记 |
| 没有中英文切换控件 | 权威检测结果必须同时包含 `README_zh.md` 和 `README.md` |
| 切换后回到另一语言首页 | 当前页面缺少同路径、同基础名的对应语言文件 |
| 首页不是预期页面 | 检查 `projects/` 根标记、`generation.default_page` 和旧构建缓存 |
| Python 依赖安装失败 | 检查代理/证书，设置 `DOCS_PIP_MIRROR` 或 `DOCS_PIP_INDEX_URL` |
| XeLaTeX 或字体失败 | 运行 `python utils/pdf_environment.py --no-auto-install` 查看精确缺失项 |
| PDF 中没有正文 | 目录 README 仅作导航时不会充当正文；需要添加普通语言文档 |
| 本地端口被占用 | 使用 `python build_local.py --serve --port 8081` |
| 多版本 worktree 失败 | 确认目标分支存在，并检查 `git worktree list` 与 Git 版本 |

需要只检查依赖而不安装：

```bash
python build_local.py --check --no-auto-install
```

需要手工安装锁定依赖：

```bash
python -m pip install -r requirements.txt
```

## 开发与验证

修改构建机制后，在 `source/` 目录执行：

```bash
python -m unittest discover -s tests -v
python build_local.py --check --no-auto-install
python build_local.py --clean
python build.py --validate
```

维护边界：

- 文档正文和图片：`projects/`
- 站点与 PDF 配置：`source/config.yaml`、`source/conf.py`
- 构建逻辑：`source/*.py`、`source/utils/`
- 网站样式与交互：`source/_static/`、`source/_templates/`
- 多版本定义：`.github/versions.json`
- CI 与 Pages：`.github/workflows/build-docs.yml`

请勿提交构建产生的 `_build/`、`source_build/`、临时 LaTeX 文件或同步副本。
