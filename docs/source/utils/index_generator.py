#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
索引生成器模块
负责生成各种索引文件（支持中英文双语）
"""

from pathlib import Path
import re
import glob
from typing import Dict, List


class IndexGenerator:
    def __init__(self, output_dir: str, file_processor):
        self.output_dir = Path(output_dir)
        self.file_processor = file_processor
        
    def get_projects_dir(self):
        """从配置中获取项目目录路径"""
        try:
            repo_config = self.file_processor.config.get('repository', {})
            projects_dir_str = repo_config.get('projects_dir', '../../projects')
            return Path(projects_dir_str)
        except (AttributeError, KeyError):
            return Path('../../projects')
    
    def find_matching_projects(self, patterns: List[str]) -> List[str]:
        """根据 patterns 查找匹配的项目"""
        projects_dir = self.get_projects_dir()
        if not projects_dir.exists():
            return []
        
        matching_projects = []
        
        for pattern in patterns:
            # 在项目目录中查找匹配的子目录
            pattern_path = projects_dir / pattern
            matches = glob.glob(str(pattern_path))
            for match in matches:
                project_path = Path(match)
                if project_path.is_dir():
                    project_name = project_path.name
                    if project_name not in matching_projects:
                        matching_projects.append(project_name)
        
        return matching_projects
    
    def has_readme_file(self, project_name: str, readme_filename: str) -> bool:
        """检查项目是否有指定的 README 文件"""
        projects_dir = self.get_projects_dir()
        project_path = projects_dir / project_name
        readme_file = project_path / readme_filename
        return readme_file.exists()

    def has_english_docs(self, projects: List[str], category: str) -> bool:
        """检查分类下是否有英文文档"""
        for project in projects:
            if self.has_readme_file(project, 'README.md'):
                return True
        return False

    def get_projects_with_lang(self, projects: List[str], category: str, lang: str) -> List[str]:
        """获取指定语言的项目列表"""
        readme_filename = 'README.md' if lang == 'en' else 'README_zh.md'
        result = []
        for project in projects:
            if self.has_readme_file(project, readme_filename):
                result.append(project)
        return result

    def generate_category_index(self, category: str, category_config: Dict, projects: List[str], lang: str = 'zh') -> str:
        """生成分类索引页面（支持中英文）"""
        if lang == 'en':
            category_name = category_config.get('name_en', category)
            title_prefix = "SDK"
            description_prefix = "This section contains"
            toctree_caption = category_config.get('name_en', category)
            summary_text = f"These examples demonstrate the {category_name.lower()} of the SDK."
        else:
            category_name = category_config.get('name', category)
            title_prefix = "SDK 的"
            description_prefix = "这里包含了 SDK 的"
            toctree_caption = category_name
            summary_text = f"这些示例展示了 SDK 的 {category_name}。"

        title_length = len(category_name)
        underline = '=' * title_length
        
        content = f"""{category_name}
{underline}

{description_prefix} {category_name}。

.. toctree::
   :maxdepth: 4
   :caption: {toctree_caption}

"""
        # 项目已经是经过语言过滤的，直接使用
        available_projects = projects
        
        # 读取各项目的显示标题，用于自然排序（数字感知、大小写不敏感）
        items = []  # (display_title, project_path)
        for project in available_projects:
            # 尝试获取标题，如果获取失败则使用项目名
            try:
                display_title = self.file_processor.get_readme_title(project, category, lang) or project
            except (AttributeError, TypeError):
                display_title = project
            items.append((display_title, project))

        # 自然排序函数
        def natural_key(s: str):
            return [int(part) if part.isdigit() else part.casefold() for part in re.split(r'(\d+)', s)]

        items.sort(key=lambda x: natural_key(x[0]))

        # 在 toctree 中使用"标题 <路径>"形式，展示更友好的名称
        readme_suffix = 'README' if lang == 'en' else 'README_zh'
        for display_title, project in items:
            content += f"   {display_title} <{project}/{readme_suffix}>\n"
        
        content += f"\n{summary_text}\n"
        return content

    def generate_main_index(self, project_info: Dict, lang: str = 'zh', categories: Dict = None) -> str:
        """生成主索引页面（支持中英文）"""
        project_name = project_info.get('name', 'SDK')
        
        if lang == 'en':
            title = f"Welcome to {project_name} Documentation!"
            intro_title = self.file_processor.get_readme_title(None, None, 'en') or "Project Introduction"
            toc_caption = "Contents"
            description = project_info.get('description_en', project_info.get('description', 'A brief introduction to the SDK.'))
        else:
            title = f"欢迎来到 {project_name} 文档！"
            intro_title = self.file_processor.get_readme_title(None, None, 'zh') or "项目简介"
            toc_caption = "目录"
            description = project_info.get('description', '这里是 SDK 的简要介绍。')

        title_length = len(title)
        underline = '=' * title_length
        intro_title_length = len(intro_title)
        intro_underline = '-' * intro_title_length

        # 读取 output_structure 以动态生成章节顺序
        output_structure = []
        # 优先使用 FileProcessor 的属性，其次使用其 config 下的 output_structure
        try:
            output_structure = (getattr(self.file_processor, 'output_structure', []) or [])
            if not output_structure:
                output_structure = ((self.file_processor.config.get('output_structure', [])) or [])
        except Exception:
            output_structure = []
        if not output_structure:
            # 回退到已有分类顺序
            output_structure = ['start', 'basic', 'driver', 'component', 'multimedia', 'multcore']
            try:
                self.structure_mode = 'hardcoded'
            except Exception:
                pass
        else:
            try:
                self.structure_mode = 'dynamic'
            except Exception:
                pass

        toc_lines = []
        lang_suffix = '_en' if lang == 'en' else ''
        for cat in output_structure:
            if categories and cat in categories:
                cat_cfg = categories.get(cat, {}) or {}
                display = (cat_cfg.get('name_en') if lang == 'en' else cat_cfg.get('name')) or cat
                toc_lines.append(f"   {display} <{cat}/index{lang_suffix}>")
            else:
                toc_lines.append(f"   {cat}/index{lang_suffix}")

        toc_block = "\n".join(toc_lines)

        content = f""".. {project_name} documentation master file, created by sphinx-quickstart

{title}
{underline}

.. toctree::
   :maxdepth: 1
   :titlesonly:

{toc_block}

{intro_title}
{intro_underline}
{description}
"""
        return content

    def write_index_file(self, content: str, file_path: str):
        """写入索引文件"""
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"已生成索引文件: {file_path}")

    def generate_all_indexes(self, categories: Dict, category_mapping: Dict, project_info: Dict):
        """生成所有索引文件（中英文）"""
        # 重新构建 category_mapping，基于配置中的 patterns
        updated_category_mapping = {}
        for category, config in categories.items():
            patterns = config.get('patterns', [])
            if patterns:
                matching_projects = self.find_matching_projects(patterns)
                updated_category_mapping[category] = matching_projects
            else:
                # 如果没有 patterns，使用原有的 mapping
                updated_category_mapping[category] = category_mapping.get(category, [])
        
        # 检查是否有英文文档
        has_any_english = False
        for category, projects in updated_category_mapping.items():
            if self.has_english_docs(projects, category):
                has_any_english = True
                break

        # 生成中文主索引（始终生成）
        main_index_content = self.generate_main_index(project_info, 'zh', categories)
        self.write_index_file(main_index_content, self.output_dir / "index.rst")

        # 如果有英文文档，生成英文主索引
        if has_any_english:
            main_index_content_en = self.generate_main_index(project_info, 'en', categories)
            self.write_index_file(main_index_content_en, self.output_dir / "index_en.rst")

        # 生成分类索引
        for category, config in categories.items():
            projects = updated_category_mapping.get(category, [])
            if projects:
                # 生成中文分类索引（始终生成）
                zh_projects = self.get_projects_with_lang(projects, category, 'zh')
                if zh_projects:
                    index_content = self.generate_category_index(category, config, zh_projects, 'zh')
                    index_path = self.output_dir / category / "index.rst"
                    self.write_index_file(index_content, index_path)

                # 如果有英文文档，生成英文分类索引
                en_projects = self.get_projects_with_lang(projects, category, 'en')
                if en_projects:
                    index_content_en = self.generate_category_index(category, config, en_projects, 'en')
                    index_path_en = self.output_dir / category / "index_en.rst"
                    self.write_index_file(index_content_en, index_path_en)

        # 末尾总结日志
        mode = getattr(self, 'structure_mode', 'unknown')
        if mode == 'from_config':
            print("索引结构生成模式: 来自配置文件 (generation.output_structure)")
        elif mode == 'from_categories':
            print("索引结构生成模式: 来自分类配置 (categories)")
        elif mode == 'empty':
            print("索引结构生成模式: 空结构 (未找到配置)")
        else:
            print(f"索引结构生成模式: {mode}")
        
        if has_any_english:
            print("检测到英文文档，已生成双语索引文件")
        else:
            print("未检测到英文文档，仅生成中文索引文件")
            
        # 打印项目发现信息
        for category, projects in updated_category_mapping.items():
            if projects:
                print(f"分类 '{category}' 发现 {len(projects)} 个项目: {', '.join(projects)}")
            else:
                print(f"分类 '{category}' 未发现项目")