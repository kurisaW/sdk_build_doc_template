# 版本与部署

发布文档时，版本不是一个显示标签，而是可重复构建的源代码快照。模板使用 .github/versions.json 声明版本入口，使用独立 Git worktree 构建每个分支，并由 GitHub Actions 对 Pull Request 和默认分支执行一致的发布规则。

## 发布链路

~~~text
versions.json
     ↓ validate
isolated Git worktrees
     ↓ build every configured version
HTML and PDF artifacts
     ↓
GitHub Pages on main or master
~~~

| 目标 | 入口 |
| --- | --- |
| 校验版本定义 | python build.py --validate |
| 查看版本矩阵 | python build.py --list-versions |
| 构建所有版本 | python build.py --clean |
| 检查当前分支 | python build_local.py --check-branch |

完整的 CI 任务划分、Artifact 留存和 Pages 发布条件见 [GitHub 自动化发布](01_github_automation_zh.md)。

:::{admonition} 发布策略建议
:class: important
把默认分支作为 latest，将受支持的稳定分支显式写入 versions.json。先让 Pull Request 完成校验和 Artifact 构建，再允许 main 或 master 部署到 Pages；不要让未验证的文档直接替换线上版本。
:::
