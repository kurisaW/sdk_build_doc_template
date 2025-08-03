# SDK 文档构建模板使用指南

## 概述

这个模板仓库提供了一套完整的SDK文档构建机制，可以帮助您快速创建专业的SDK文档网站。

## 核心特性

### 🚀 自动化文档生成
- 自动扫描项目目录结构
- 根据命名规则自动分类
- 生成统一的文档导航
- 支持Markdown和RST格式

### 📚 多版本支持
- 支持多个分支版本
- 自动生成版本切换菜单
- 版本间文档完全隔离
- 支持版本回退

### 🌐 多平台部署
- GitHub Pages自动部署
- Read the Docs集成
- 本地预览支持
- 自定义域名支持

### 🎨 现代化界面
- 响应式设计
- 深色/浅色主题
- 全文搜索功能
- 移动端优化

## 快速开始

### 1. 使用模板

1. 点击仓库页面的 "Use this template" 按钮
2. 选择 "Create a new repository"
3. 填写仓库名称和描述
4. 点击 "Create repository from template"

### 2. 配置项目

```bash
# 克隆新创建的仓库
git clone https://github.com/your-username/your-sdk-repo.git
cd your-sdk-repo

# 进入source目录
cd source

# 运行项目设置脚本
python setup_new_project.py
```

按照提示填写项目信息：
- SDK文档名称
- SDK文档标题
- 项目描述
- 版本号
- 作者信息
- 版权信息
- 仓库名称
- SDK项目前缀

### 3. 添加项目

在 `projects/` 目录下添加您的示例项目：

```bash
# 创建新项目目录
mkdir projects/my_sdk_basic_led
mkdir projects/my_sdk_driver_uart
mkdir projects/my_sdk_component_mqtt

# 为每个项目添加README.md文件
```

### 4. 构建文档

```bash
# 检查依赖
python build_local.py --check

# 构建文档
python build_local.py

# 本地预览
python build_local.py --serve
```

### 5. 部署文档

#### GitHub Pages (推荐)

推送到 `master` 或 `main` 分支，GitHub Actions会自动构建并部署：

```bash
git add .
git commit -m "Add new projects"
git push origin main
```

#### Read the Docs

1. 在 [Read the Docs](https://readthedocs.org/) 上注册账号
2. 导入您的GitHub仓库
3. 选择 `source/conf.py` 作为配置文件
4. 构建会自动开始

## 项目结构说明

### 目录结构

```
your-sdk-repo/
├── source/                    # 文档构建核心
│   ├── conf.py               # Sphinx配置
│   ├── config.yaml           # 项目配置
│   ├── build_local.py        # 本地构建脚本
│   ├── doc_generator.py      # 文档生成器
│   ├── version_generator.py  # 版本生成器
│   ├── setup_new_project.py  # 项目设置脚本
│   ├── requirements.txt      # Python依赖
│   └── _static/             # 静态资源
├── projects/                 # 示例项目
│   ├── basic_example/       # 基础示例
│   ├── driver_example/      # 驱动示例
│   └── component_example/   # 组件示例
├── .github/workflows/       # GitHub Actions
├── .readthedocs.yaml        # Read the Docs配置
└── README.md               # 项目说明
```

### 配置文件

#### config.yaml

主要的项目配置文件，包含：

```yaml
project:
  name: "Your_SDK_Docs"
  title: "Your SDK 文档"
  description: "SDK文档描述"
  version: "1.0.0"
  author: "Your Name"
  copyright: "2025, Your Company"

categories:
  basic:
    name: "基础篇"
    description: "基础功能示例"
    patterns:
      - "basic_*"
  
  driver:
    name: "驱动篇"
    description: "外设驱动示例"
    patterns:
      - "driver_*"
```

#### conf.py

Sphinx配置文件，控制文档构建的各个方面：

```python
# 项目信息
project = 'Your SDK Docs'
copyright = '2025, Your Company'
author = 'Your Name'

# 主题配置
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'titles_only': False,
}
```

## 文档分类规则

### 自动分类

系统会根据项目名称自动分类：

- `basic_*` → 基础篇
- `driver_*` → 驱动篇
- `component_*` → 组件篇
- `protocol_*` → 协议篇

### 自定义分类

在 `config.yaml` 中修改 `categories` 部分：

```yaml
categories:
  tutorial:
    name: "教程篇"
    description: "入门教程"
    patterns:
      - "tutorial_*"
  
  advanced:
    name: "高级篇"
    description: "高级功能"
    patterns:
      - "advanced_*"
```

## 多版本管理

### 版本配置

在 `.github/versions.list` 中配置版本：

```
# 版本列表
master
v1.0
v1.1
v2.0
```

### 分支对应

- `main` 分支 → `latest` 版本
- `v1.0` 分支 → `v1.0` 版本
- `v1.1` 分支 → `v1.1` 版本

### 版本切换

用户可以通过版本菜单在不同版本间切换，每个版本的文档完全独立。

## 自定义主题

### 修改主题

在 `source/conf.py` 中修改主题配置：

```python
# 使用其他主题
html_theme = 'sphinx_rtd_theme'

# 主题选项
html_theme_options = {
    'navigation_depth': 4,
    'titles_only': False,
    'collapse_navigation': False,
    'sticky_navigation': True,
}
```

### 添加自定义CSS/JS

1. 在 `source/_static/` 目录下添加文件
2. 在 `conf.py` 中引用：

```python
html_css_files = ['custom.css']
html_js_files = ['custom.js']
```

## 故障排除

### 常见问题

**Q: 构建失败怎么办？**
A: 检查Python依赖，运行 `pip install -r requirements.txt`

**Q: 文档没有自动分类？**
A: 检查项目命名是否符合规则，或修改 `config.yaml` 中的模式匹配

**Q: GitHub Pages部署失败？**
A: 检查 `.github/workflows/gh-pages.yml` 文件是否正确

**Q: 版本切换不工作？**
A: 确保在 `.github/versions.list` 中正确配置了版本

### 调试命令

```bash
# 检查依赖
python build_local.py --check

# 详细输出
python build_local.py --verbose

# 清理构建
python build_local.py --clean

# 检查分支版本
python build_local.py --check-branch

# 构建所有版本
python build_local.py --all-versions
```

### 日志分析

构建过程中的日志会显示：
- 项目扫描结果
- 分类匹配情况
- 文档生成状态
- 错误信息

## 最佳实践

### 项目命名

- 使用有意义的名称
- 遵循命名规则
- 保持一致性

### 文档结构

- 每个项目都有README.md
- 包含功能说明
- 提供使用示例
- 添加注意事项

### 版本管理

- 使用语义化版本号
- 保持版本历史
- 及时更新文档

### 持续集成

- 启用GitHub Actions
- 配置Read the Docs
- 定期检查构建状态

## 扩展功能

### 添加新功能

1. 修改 `source/doc_generator.py`
2. 更新配置文件
3. 测试新功能
4. 更新文档

### 自定义构建

1. 修改 `source/build_local.py`
2. 添加新的构建选项
3. 更新命令行参数
4. 测试构建流程

## 支持与贡献

### 获取帮助

- 查看 [Issues](../../issues) 页面
- 创建新的 Issue
- 提供详细的错误信息

### 贡献代码

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 打开 Pull Request

### 反馈建议

欢迎提出改进建议和功能需求，帮助我们不断完善这个模板。

---

**让SDK文档构建变得简单高效！** 🚀 