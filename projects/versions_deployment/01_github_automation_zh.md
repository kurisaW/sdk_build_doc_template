# GitHub Actions 与 GitHub Pages 自动发布

仓库内置 workflow 监听 source、projects 和 versions.json 的变化。它把“配置可解析”“PDF 环境可用”“所有版本可以构建”“产物能部署”拆成可观察的阶段，而不是在最后一步才发现问题。

## 工作流阶段

| Job 或步骤 | 责任 | 结果 |
| --- | --- | --- |
| validate-versions | 安装 Python 3.11 与依赖，运行 build.py --validate | 阻止无效版本配置进入构建 |
| build-docs | 安装 XeLaTeX、字体和 locale，验证 PDF 环境 | 为每个版本生成 HTML 和 PDF |
| upload-artifact | 上传 source/source_build/html | Pull Request 上可下载并人工验收 |
| deploy-docs | 仅在 main 或 master 下载 Artifact 并发布 | GitHub Pages 更新到孤儿分支 |

## PR 与默认分支的行为差异

Pull Request 会运行校验和构建，但不会部署；这给评审者一个可下载 Artifact，用来检查导航、语言切换、搜索和 PDF。合并到 main 或 master 后，deploy-docs 通过 peaceiris/actions-gh-pages 发布同一份 Artifact，并以 force_orphan 保持发布分支只保存静态站点。

## 发布前检查清单

- versions.json 已通过 build.py --validate。
- 无 PDF 的本地构建已通过，且深层页面和图片可访问。
- 在具备 XeLaTeX 与精确字体的环境中已完成完整 PDF 构建。
- 英文和中文页面都检查过搜索与切换回退。
- Artifact 内容与 Pages 入口版本一致。

触发条件和环境安装命令在 .github/workflows/build-docs.yml 中；不建议把关键依赖只安装在本地而遗漏 CI。
