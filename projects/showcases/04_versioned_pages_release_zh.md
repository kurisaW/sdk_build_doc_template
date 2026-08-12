# 示例：多版本 GitHub Pages 发布

## 场景

开源 SDK 的 main 分支持续迭代，但用户仍需要 v1.1 的安装命令和 API 说明。将 latest 和稳定分支同时发布，既保证新读者看到当前能力，也避免历史使用者被不兼容修改打断。

~~~json
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
      "name": "v1.1",
      "display_name": "v1.1",
      "branch": "v1.1",
      "url_path": "v1.1",
      "description": "稳定维护版本"
    }
  ],
  "default_version": "main",
  "latest_version": "main"
}
~~~

构建器不会 checkout 当前工作目录，而是为 main 和 v1.1 分别建立 worktree。PR 阶段产出 Artifact 供评审；合并到默认分支后，部署任务将相同 Artifact 发布到 GitHub Pages。版本菜单只需读取构建时注入的版本描述，无需手工维护静态链接。
