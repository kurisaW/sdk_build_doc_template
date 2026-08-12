# 快速开始

这一章的目标不是“成功运行一个命令”，而是用最短路径验证内容发现、语言识别、HTML 构建和发布入口是否符合预期。首次尝试建议先跳过 PDF，确认网页流程无误后再准备 XeLaTeX 环境。

## 五分钟路径

1. 克隆或通过 Use this template 创建仓库。
2. 创建 Python 3.11 虚拟环境，并进入 source 目录。
3. 使用检查模式确认依赖和配置。
4. 运行无 PDF 的本地构建并打开静态站点。
5. 提交到 main 或 master，让 GitHub Actions 做完整的 PDF 与多版本验证。

~~~powershell
git clone https://github.com/your-org/your-docs.git
cd your-docs
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
cd source
python build_local.py --check
python build_local.py --clean --no-pdf --serve
~~~

浏览器访问 http://localhost:8000。构建细节、输出目录和所有命令参数见 [首次本地构建](01_first_build_zh.md)。

:::{admonition} PDF 是正式交付检查，而不是第一个阻碍
:class: note
HTML 预览只需要 Python 依赖；PDF 还需要 XeLaTeX 与精确字体。日常写作可使用 --no-pdf 保持反馈速度，合并或发布前再运行完整构建。
:::
