# 首次本地构建

在 source 目录执行以下命令。脚本会读取 config.yaml、检查锁定的 Python 依赖、同步 projects 内容、生成导航并分别构建语言站点。

~~~bash
python build_local.py --check
python build_local.py --clean --no-pdf
python build_local.py --clean --no-pdf --serve --port 8000
~~~

## 预期产物

| 路径 | 用途 |
| --- | --- |
| source/_build/html/index.html | 本地稳定入口，会跳转到默认语言首页 |
| source/_build/html/ | HTML、搜索索引和静态资源 |
| source/_build/html/_static/ | 下载 PDF 和运行时页面资源 |
| source/_build/latex/ | PDF 中间产物，成功后会清理 |

若依赖缺失，脚本默认尝试安装可用版本；在受控环境中加上 --no-auto-install，使其只报告差异。执行 --clean 会清理旧 HTML，避免已删除页面仍残留在搜索或导航中。

## 首次失败时先做什么

先运行 python build_local.py --check --no-auto-install，确认 Python 环境与 requirements.txt 相符。若 HTML 可以生成但 PDF 失败，不要尝试用本机替代字体绕过错误；请转到 [PDF 交付](../build_outputs/02_pdf_delivery_zh.md) 按名称安装配置要求的字体。
