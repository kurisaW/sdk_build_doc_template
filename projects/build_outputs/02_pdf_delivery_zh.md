# PDF 交付：排版与环境同样是构建输入

PDF 不是从浏览器打印网页。模板固定使用 Sphinx LaTeX 到 XeLaTeX 的路径，并在开始排版前验证工具和精确字体。中文和英文按实际检测到的语言分别生成 PDF。

~~~text
DocumentCatalog
      ↓
Sphinx LaTeX builder
      ↓
XeLaTeX + configured fonts
      ↓
validated Chinese / English PDF
~~~

## 输出特征

封面、目录、页眉、页码、书签和章节分页由 LaTeX 配置统一控制。表格、代码块、行内代码、图片和 WebP 均有专门处理；PDF_STYLE 可在 web、thesis、graduate 和 academic 之间选择。

~~~bash
python utils/pdf_environment.py --no-auto-install
python build_local.py --clean
~~~

生成文件位于 source/_build/html/_static，中文文件名通常是 SDK_Docs_Template.pdf，英文文件名以 _EN.pdf 结尾。

:::{admonition} 严格字体校验是有意设计
:class: warning
字体缺失时构建会失败，不会静默回退到相近字体。这样才能避免本地正常、CI 乱码，或不同机器的分页和代码宽度不一致。
:::
