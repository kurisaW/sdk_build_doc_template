# 问题排查

遇到构建失败时，先根据错误所属阶段缩小范围。不要直接删除 source 中的临时文件或修改生成导航；这些文件由构建器清单管理，下一次成功构建会自动清理。

| 现象 | 首先检查 | 推荐命令 |
| --- | --- | --- |
| 页面或图片缺失 | projects 中的相对路径、文件后缀、目录范围 | python build_local.py --clean --no-pdf |
| 双语按钮不存在或跳转首页 | 根 README 对、同名翻译文件 | python build_local.py --clean --no-pdf |
| 分类为空或项目重复 | patterns、entry_files、duplicate_categories | python build.py --validate |
| PDF 字体或 XeLaTeX 失败 | config.yaml 字体名和 pdf_environment | python utils/pdf_environment.py --no-auto-install |
| CI 与本地不一致 | Python 版本、requirements、字体、locale | 对照 workflow 的安装步骤 |

## 排查顺序

1. 运行 --check --no-auto-install，记录依赖差异。
2. 运行 --clean --no-pdf，先把内容与导航问题同 PDF 环境问题分开。
3. 检查生成目录中目标语言的页面和图片。
4. 再运行完整 PDF 构建，按缺失工具或精确字体修复。
5. 最后对照 GitHub Actions Artifact，而不是只看 Pages 缓存。
