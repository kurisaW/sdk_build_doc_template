# 示例：嵌入式 SDK 开发手册

## 场景

一个传感器 SDK 同时需要安装、初始化、数据采集、错误码和板级排错文档。读者会沿着学习路径阅读，因此选择 recursive_tree，让目录结构直接成为导航结构。

~~~text
projects/
├── getting_started/
│   ├── README_zh.md
│   ├── install_zh.md
│   └── first_sample_zh.md
├── api_reference/
│   ├── README_zh.md
│   └── sensor_stream_zh.md
└── troubleshooting/
    ├── README_zh.md
    └── i2c_diagnostics_zh.md
~~~

## 内容策略

- 安装页面给出操作系统、工具链和最低 SDK 版本。
- API 页面使用表格描述参数，使用可复制的代码块描述最小调用。
- 排错页面按症状、证据、原因和修复顺序编写，而不是按模块名堆叠。
- 同名中英文文件让语言切换保留阅读上下文。

## 验收

运行 python build_local.py --clean --no-pdf --serve 后，检查从安装页到 API 页的侧栏连续性、代码块复制体验、图片分辨率和中英文对应页。发布前再运行完整 PDF，确认长表格和代码没有越界。
