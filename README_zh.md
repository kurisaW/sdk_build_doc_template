# SDK 文档构建模板

[**English**](./README.md) | **中文**

## 简介

这是一个专为SDK文档构建设计的GitHub模板仓库。它提供了一套完整的自动化文档构建机制，能够：

- 🚀 **自动生成文档结构** - 根据项目目录自动分类和生成文档
- 📚 **多版本支持** - 支持多个版本的文档构建和切换
- 🌐 **多平台部署** - 支持GitHub Pages和Read the Docs部署
- 🎨 **现代化界面** - 基于Sphinx和Read the Docs主题的美观界面
- 🔧 **易于配置** - 通过YAML配置文件快速定制

## 目录结构

```
sdk-docs-template/
├── source/                    # 文档构建核心目录
│   ├── conf.py               # Sphinx配置文件
│   ├── config.yaml           # 项目配置文件
│   ├── build_local.py        # 本地构建脚本
│   ├── doc_generator.py      # 文档生成器
│   ├── version_generator.py  # 版本生成器
│   ├── setup_new_project.py  # 新项目设置脚本
│   ├── requirements.txt      # Python依赖
│   └── _static/             # 静态资源
├── projects/                 # 示例项目目录
│   ├── basic_example/       # 基础示例
│   ├── driver_example/      # 驱动示例
│   └── component_example/   # 组件示例
├── .github/workflows/       # GitHub Actions工作流
├── .readthedocs.yaml        # Read the Docs配置
└── README.md               # 项目说明
```

## 快速开始

### 1. 使用模板创建新仓库

1. 点击 "Use this template" 按钮
2. 选择 "Create a new repository"
3. 填写仓库名称和描述
4. 点击 "Create repository from template"

### 2. 配置项目

```bash
# 进入source目录
cd source

# 运行项目设置脚本
python setup_new_project.py
```

按照提示填写项目信息，脚本会自动生成配置文件。

### 3. 构建文档

```bash
# 检查依赖
python build_local.py --check

# 构建文档
python build_local.py

# 本地预览
python build_local.py --serve
```

### 4. 部署文档

#### GitHub Pages (推荐)

推送到 `master` 或 `main` 分支，GitHub Actions会自动构建并部署到GitHub Pages。

#### Read the Docs

1. 在Read the Docs上连接你的仓库
2. 选择 `source/conf.py` 作为配置文件
3. 构建会自动开始

## 配置说明

### 项目配置 (config.yaml)

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

### 文档分类

系统支持以下文档分类：

- **基础篇** - 基础功能示例
- **驱动篇** - 外设驱动示例  
- **组件篇** - 网络组件示例
- **协议篇** - 工业协议示例

### 项目命名规则

文档生成器会根据项目名称模式自动分类：

- `basic_*` → 基础篇
- `driver_*` → 驱动篇
- `component_*` → 组件篇
- `protocol_*` → 协议篇

## 功能特性

### 🔄 自动化文档生成

- 自动扫描项目目录
- 根据命名规则分类
- 生成统一的文档结构
- 支持Markdown和RST格式

### 📋 多版本管理

- 支持多个分支版本
- 自动生成版本切换菜单
- 版本间文档隔离

### 🎨 现代化界面

- 响应式设计
- 深色/浅色主题
- 搜索功能
- 移动端适配

### ⚡ 快速构建

- 增量构建
- 并行处理
- 缓存机制
- 本地预览

## 开发指南

### 添加新项目

1. 在 `projects/` 目录下创建新项目
2. 按照命名规则命名项目
3. 添加 `README.md` 文件
4. 运行构建脚本

### 自定义主题

修改 `source/conf.py` 中的主题配置：

```python
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'titles_only': False,
}
```

### 添加自定义CSS/JS

在 `source/_static/` 目录下添加静态文件，在 `conf.py` 中引用：

```python
html_css_files = ['custom.css']
html_js_files = ['custom.js']
```

## 故障排除

### 常见问题

**Q: 构建失败怎么办？**
A: 检查Python依赖是否正确安装，运行 `pip install -r requirements.txt`

**Q: 文档没有自动分类？**
A: 检查项目命名是否符合规则，或修改 `config.yaml` 中的模式匹配

**Q: GitHub Pages部署失败？**
A: 检查 `.github/workflows/gh-pages.yml` 文件是否正确

### 调试模式

```bash
# 详细输出
python build_local.py --verbose

# 清理构建
python build_local.py --clean

# 检查分支版本
python build_local.py --check-branch
```

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 Apache License 2.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 支持

如果您在使用过程中遇到问题，请：

1. 查看 [Issues](../../issues) 页面
2. 创建新的 Issue 描述问题
3. 提供详细的错误信息和复现步骤

---

**让SDK文档构建变得简单高效！** 🚀
