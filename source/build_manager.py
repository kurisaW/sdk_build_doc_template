#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中央构建管理器
完全基于 .github/versions.json 动态生成分支名称和构建配置
支持 Git Worktree 隔离构建，避免分支切换问题
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import yaml
from utils.html_builder import build_html_site, write_site_entry
from utils.language_support import (
    configured_language_paths,
    detect_languages,
    select_default_language,
)
from utils.pdf_builder import build_detected_pdfs
from utils.pdf_environment import ensure_pdf_environment

class VersionConfig:
    """版本配置类"""
    def __init__(self, config_dict: Dict):
        self.name = config_dict['name']
        self.display_name = config_dict['display_name']
        self.branch = config_dict['branch']
        self.url_path = config_dict['url_path']
        self.description = config_dict.get('description', '')

class BuildManager:
    """构建管理器"""
    
    def __init__(self):
        self.project_root = self._find_project_root()
        self.versions_file = self.project_root / '.github' / 'versions.json'
        self.docs_source = self.project_root / 'source'
        # 统一切换到新的构建输出根目录: source_build/html/<version>
        self.build_root = self.docs_source / 'source_build'
        self.worktrees_dir = self.build_root / 'worktrees'
        self.versions_dir = self.build_root / 'html'
        
        
    def _find_project_root(self) -> Path:
        """查找项目根目录"""
        current = Path.cwd()
        while current != current.parent:
            if (current / '.github' / 'versions.json').exists():
                return current
            current = current.parent
        raise FileNotFoundError("找不到 .github/versions.json 文件")
    
    def load_versions_config(self) -> Dict:
        """加载版本配置文件"""
        try:
            with open(self.versions_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"[OK] 加载版本配置: {[v['name'] for v in config.get('versions', [])]}")
            return config
        except Exception as e:
            print(f"[ERROR] 无法加载版本配置: {e}")
            return {'versions': [], 'default_version': '', 'latest_version': ''}
    
    def get_version_configs(self) -> List[VersionConfig]:
        """获取版本配置列表"""
        config = self.load_versions_config()
        versions = []
        for version_dict in config.get('versions', []):
            versions.append(VersionConfig(version_dict))
        return versions

    def _sphinx_environment(
        self, environment: Dict[str, str], docs_source: Optional[Path] = None
    ) -> Dict[str, str]:
        """Make source helper modules importable from any version worktree."""
        source_paths = [
            str(path.resolve())
            for path in (docs_source, self.docs_source)
            if path is not None and path.exists()
        ]
        current = environment.get('PYTHONPATH', '')
        environment['PYTHONPATH'] = os.pathsep.join(
            dict.fromkeys(item for item in (*source_paths, current) if item)
        )
        return environment
    
    def create_worktree(self, version_config: VersionConfig) -> Path:
        """为指定版本创建 Git worktree"""
        worktree_path = self.worktrees_dir / version_config.name
        
        # 获取当前分支
        current_branch = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True, text=True, check=True
        ).stdout.strip()

        # GitHub Actions checks pull requests out as a detached commit.  There
        # is no local branch to create a worktree from in that state, and
        # falling back to the configured branch would build the base branch
        # instead of the commit that triggered this run.
        if current_branch == 'HEAD':
            print("当前检出为 detached HEAD，直接使用 PR 检出目录")
            return Path.cwd()
        
        # 如果目标分支就是当前分支，直接使用当前目录
        if version_config.branch == current_branch:
            print(f"目标分支 {version_config.branch} 就是当前分支，使用当前目录")
            return Path.cwd()
        
        # 清理已存在的 worktree
        if worktree_path.exists():
            print(f"清理已存在的 worktree: {worktree_path}")
            try:
                subprocess.run(['git', 'worktree', 'remove', str(worktree_path)], 
                             check=True, capture_output=True)
            except subprocess.CalledProcessError:
                # 如果 worktree remove 失败，手动删除
                shutil.rmtree(worktree_path, ignore_errors=True)
        
        # 创建新的 worktree
        print(f"创建 worktree: {version_config.branch} -> {worktree_path}")
        subprocess.run([
            'git', 'worktree', 'add', 
            str(worktree_path), version_config.branch
        ], check=True)
        
        return worktree_path

    def _build_html_and_pdf(
        self, docs_source: Path, version_config: VersionConfig, config: Dict
    ) -> bool:
        """按语言隔离构建文档，再合并为统一静态站点。"""
        output_dir = self.build_root / 'html' / version_config.url_path
        output_dir.mkdir(parents=True, exist_ok=True)
        project_config = config.get('project', {}) or {}
        generation = config.get('generation', {}) or {}
        available_languages = detect_languages(docs_source, generation)
        default_language = select_default_language(
            available_languages, generation
        )
        detected_label = '、'.join(available_languages) or '未检测到 README 语言标记'
        print(
            f"构建目录树文档: {output_dir} "
            f"(语言: {detected_label}; 默认: {default_language})"
        )
        language_roots = build_html_site(
            docs_source,
            output_dir,
            config,
            available_languages,
            default_language,
        )
        project_title = project_config.get(
            'title', project_config.get('name', 'SDK 文档')
        )
        write_site_entry(
            output_dir,
            language_roots[default_language],
            project_title,
            default_language,
        )

        pdf_success, pdf_files = build_detected_pdfs(
            output_dir,
            docs_source,
            config,
            languages=available_languages,
            auto_install=True,
        )
        if not pdf_success:
            print(f"[ERROR] 版本 {version_config.display_name} 的 PDF 生成失败")
            return False
        for pdf_file in pdf_files:
            print(f"[OK] PDF文档: {pdf_file}")

        projects_dir_web = ''
        configured_projects_dir = str(
            (config.get('repository', {}) or {}).get('projects_dir', '') or ''
        ).replace('\\', '/')
        path_parts = [
            part for part in configured_projects_dir.split('/')
            if part not in {'', '.', '..'}
        ]
        if path_parts:
            projects_dir_web = path_parts[-1]
        directory_index_files = list(
            configured_language_paths(generation, 'directory_index').values()
        )
        self._generate_version_config(
            output_dir,
            version_config,
            projects_dir_web,
            directory_index_files,
        )
        self._ensure_version_index(output_dir, config)
        return True
    
    def build_docs_in_worktree(self, worktree_path: Path, version_config: VersionConfig) -> bool:
        """在 worktree 中构建文档"""
        print(f"在 worktree 中构建文档: {worktree_path}")
        
        # 检查 source 目录是否存在
        if worktree_path == Path.cwd():
            # 如果是当前分支，使用主分支的 source 目录
            docs_source_in_worktree = self.docs_source
        else:
            docs_source_in_worktree = worktree_path / 'source'
            if not docs_source_in_worktree.exists():
                print(f"[WARN]  警告: {worktree_path} 中没有 source 目录")
                print(f"   使用主分支的文档结构进行构建")
                # 复制主分支的文档结构
                main_docs = self.docs_source
                if main_docs.exists():
                    shutil.copytree(main_docs, docs_source_in_worktree, dirs_exist_ok=True)
                else:
                    print(f"[ERROR] 错误: 主分支也没有 source 目录")
                    return False
        
        # 切换到 worktree 目录（如果不是当前分支）
        if worktree_path != Path.cwd():
            os.chdir(worktree_path)
        
        try:
            # 运行文档生成脚本（如果存在）
            doc_generator = docs_source_in_worktree / 'doc_generator.py'
            if doc_generator.exists():
                print(f"运行文档生成脚本: {doc_generator}")
                subprocess.run([sys.executable, str(doc_generator)], 
                             cwd=str(docs_source_in_worktree), check=True)
            
            # 嵌入版本配置
            embed_script = docs_source_in_worktree / 'utils' / 'embed_version_config.py'
            if embed_script.exists():
                print(f"嵌入版本配置: {embed_script}")
                subprocess.run([sys.executable, str(embed_script)], 
                             cwd=str(docs_source_in_worktree), check=True)

            cfg_path = docs_source_in_worktree / 'config.yaml'
            with open(cfg_path, 'r', encoding='utf-8') as f:
                build_config = yaml.safe_load(f) or {}
            return self._build_html_and_pdf(
                docs_source_in_worktree, version_config, build_config
            )

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] 构建失败: {e}")
            return False
        finally:
            # 恢复到原始目录（如果不是当前分支）
            if worktree_path != Path.cwd():
                os.chdir(self.project_root)
    
    def _generate_version_config(self, output_dir: Path, version_config: VersionConfig, projects_dir_web: str = '', copy_files: list = None):
        """生成版本切换配置文件
        projects_dir_web: 仓库内项目根路径（URL 片段），例如 "project" 或 "projects/examples"
        """
        config = self.load_versions_config()
        
        # 创建版本配置 JSON 文件 - 修复格式
        version_config_file = output_dir / 'version_config.json'
        with open(version_config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        # 创建版本信息 HTML 文件
        version_info_file = output_dir / 'version_info.html'
        version_info_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>版本信息</title>
</head>
<body>
    <script>
        window.versionInfo = {{
            "name": "{version_config.name}",
            "display_name": "{version_config.display_name}",
            "branch": "{version_config.branch}",
            "url_path": "{version_config.url_path}",
            "description": "{version_config.description}"
        }};
    </script>
</body>
</html>"""
        
        with open(version_info_file, 'w', encoding='utf-8') as f:
            f.write(version_info_html)
        
        # 同时创建 _static 目录下的配置文件
        static_dir = output_dir / '_static'
        static_dir.mkdir(exist_ok=True)
        static_config_file = static_dir / 'version_config.json'
        with open(static_config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        # 生成可直接加载的 JS，提供 window.versionInfo（含当前版本信息）
        version_info_js = static_dir / 'version_info.js'
        version_info_obj = {
            "name": version_config.name,
            "display_name": version_config.display_name,
            "branch": version_config.branch,
            "url_path": version_config.url_path,
            "description": version_config.description,
            "projectsDir": projects_dir_web or '',
            "copyFiles": copy_files or []
        }
        with open(version_info_js, 'w', encoding='utf-8') as f:
            f.write("window.versionInfo = " + json.dumps(version_info_obj, ensure_ascii=False) + ";\n")
        
        print(f"[OK] 生成版本配置文件: {version_config_file}")
        print(f"[OK] 生成静态配置文件: {static_config_file}")

    def _ensure_version_index(self, output_dir: Path, config: Dict) -> None:
        """Create a stable version entry page for GitHub Pages deployments."""
        index_file = output_dir / 'index.html'
        if index_file.is_file():
            return

        generation = config.get('generation', {}) or {}
        default_language = str(generation.get('default_language', 'zh') or 'zh')
        candidates = (
            ('README_zh.html', 'README.html')
            if default_language == 'zh'
            else ('README.html', 'README_zh.html')
        )
        target = next((name for name in candidates if (output_dir / name).is_file()), None)
        if target is None:
            target = next(
                (path.name for path in output_dir.glob('*.html') if path.name != 'index.html'),
                None,
            )
        if target is None:
            raise FileNotFoundError(
                f'版本输出目录没有可用 HTML 首页: {output_dir}'
            )

        index_file.write_text(
            '<!doctype html>\n'
            '<html lang="zh-CN"><head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<meta http-equiv="refresh" content="0; url=./{target}">\n'
            f'<title>SDK 文档</title></head><body>\n'
            f'<p><a href="./{target}">打开文档</a></p>\n'
            '</body></html>\n',
            encoding='utf-8',
        )
        print(f'[OK] 创建版本入口页面: {index_file} -> {target}')
    
    
    def copy_build_result(self, worktree_path: Path, version_config: VersionConfig):
        """就地构建后无需复制，保持接口以兼容调用方"""
        target_dir = self.versions_dir / version_config.url_path
        if target_dir.exists():
            print(f"[OK] 构建结果已在目标目录: {target_dir}")
            return True
        else:
            print(f"[ERROR] 目标目录不存在: {target_dir}")
            return False

    def _generate_pdf_latex(self, docs_source_in_worktree: Path, version_config: VersionConfig) -> Optional[Path]:
        """使用传统LaTeX方法生成PDF（作为回退方案）"""
        self._ensure_pdf_dependencies()
        pdf_file = None
        
        try:
            # 尝试 latexpdf 构建器
            latexpdf_dir = self.build_root / 'latexpdf' / version_config.url_path
            print(f"尝试使用 latexpdf 构建: {latexpdf_dir}")
            sphinx_env = self._sphinx_environment(
                os.environ.copy(), docs_source_in_worktree
            )
            subprocess.run([
                sys.executable, '-m', 'sphinx.cmd.build',
                '-b', 'latexpdf',
                str(docs_source_in_worktree),
                str(latexpdf_dir)
            ], check=True, env=sphinx_env)

            # 预期输出：conf.py 设定主文档名 sdk-docs.tex -> sdk-docs.pdf
            candidate = latexpdf_dir / 'sdk-docs.pdf'
            if candidate.exists():
                pdf_file = candidate
            else:
                # 回退查找任意 pdf
                pdf_candidates = list(latexpdf_dir.glob('*.pdf'))
                if pdf_candidates:
                    pdf_file = pdf_candidates[0]
        except subprocess.CalledProcessError:
            # 回退到 latex + 编译链
            latex_dir = self.build_root / 'latex' / version_config.url_path
            print(f"latexpdf 失败，回退到 LaTeX 构建: {latex_dir}")
            subprocess.run([
                sys.executable, '-m', 'sphinx.cmd.build',
                '-b', 'latex',
                str(docs_source_in_worktree),
                str(latex_dir)
            ], check=True, env=sphinx_env)

            try:
                tex_files = list(latex_dir.glob('*.tex'))
                main_tex = None
                # 优先使用 conf.py 指定的 sdk-docs.tex
                candidate_tex = latex_dir / 'sdk-docs.tex'
                if candidate_tex.exists():
                    main_tex = candidate_tex
                elif tex_files:
                    main_tex = tex_files[0]

                if main_tex:
                    # latexmk -> tectonic -> pdflatex
                    compiled = False
                    try:
                        subprocess.run(['latexmk', '-pdf', '-silent', '-interaction=nonstopmode', str(main_tex.name)], cwd=str(latex_dir), check=True)
                        compiled = True
                    except Exception:
                        try:
                            subprocess.run(['tectonic', str(main_tex.name)], cwd=str(latex_dir), check=True)
                            compiled = True
                        except Exception:
                            try:
                                subprocess.run(['pdflatex', '-interaction=nonstopmode', str(main_tex.name)], cwd=str(latex_dir), check=True)
                                subprocess.run(['pdflatex', '-interaction=nonstopmode', str(main_tex.name)], cwd=str(latex_dir), check=True)
                                compiled = True
                            except Exception:
                                pass

                    if compiled:
                        # 优先 sdk-docs.pdf
                        candidate_pdf = latex_dir / 'sdk-docs.pdf'
                        if candidate_pdf.exists():
                            pdf_file = candidate_pdf
                        else:
                            pdf_candidates = list(latex_dir.glob('*.pdf'))
                            if pdf_candidates:
                                pdf_file = pdf_candidates[0]
            except Exception as e:
                print(f"[WARN]  LaTeX 回退编译失败: {e}")
        
        return pdf_file

    def _ensure_pdf_dependencies(self, config: Optional[Dict] = None) -> bool:
        """Require the shared XeLaTeX/font environment used by local and CI builds."""
        if config is None:
            config_path = self.docs_source / 'config.yaml'
            try:
                with open(config_path, 'r', encoding='utf-8') as stream:
                    config = yaml.safe_load(stream) or {}
            except (OSError, yaml.YAMLError) as exc:
                print(f"[ERROR] Unable to read PDF font configuration: {exc}")
                return False
        return ensure_pdf_environment(config, auto_install=True)
    
    def cleanup_worktree(self, worktree_path: Path):
        """清理 worktree：仅对 source_build/worktrees 下的有效 worktree 执行删除"""
        if not worktree_path.exists():
            return

        # 仅在我们的临时 worktrees 根目录下才允许删除
        try:
            worktree_root = self.worktrees_dir.resolve()
            candidate = worktree_path.resolve()
            is_under_root = str(candidate).startswith(str(worktree_root))
        except Exception:
            is_under_root = False

        if not is_under_root:
            # 避免误删非临时目录（例如当前仓库根或任意外部路径）
            return

        # 在删除之前确认它是一个已登记的 git worktree
        is_git_worktree = False
        try:
            listed = subprocess.run(['git', 'worktree', 'list'], capture_output=True, text=True, check=True).stdout
            is_git_worktree = str(candidate) in listed
        except Exception:
            pass

        if is_git_worktree:
            # 尝试优先用 git worktree remove --force
            for args in (["git", "worktree", "remove", "--force", str(candidate)],
                         ["git", "worktree", "remove", str(candidate)]):
                try:
                    subprocess.run(args, check=True, capture_output=True)
                    print(f"[OK] 清理 worktree: {worktree_path}")
                    return
                except subprocess.CalledProcessError:
                    continue

        # 兜底：非登记 worktree 或命令失败，做文件系统级别删除
        shutil.rmtree(candidate, ignore_errors=True)
    
    def build_all_versions(self, clean=False):
        """构建所有版本"""
        print("=" * 60)
        print("开始构建所有版本")
        print("=" * 60)
        
        if clean:
            print("清理构建目录...")
            if self.build_root.exists():
                shutil.rmtree(self.build_root)
        
        # 确保构建目录存在
        self.build_root.mkdir(parents=True, exist_ok=True)
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载版本配置
        versions = self.get_version_configs()
        print(f"[OK] 加载版本配置: {[v.name for v in versions]}")
        
        success_count = 0
        total_count = len(versions)
        
        for version_config in versions:
            print("\n" + "=" * 40)
            print(f"构建版本: {version_config.display_name} ({version_config.branch})")
            print("=" * 40)
            
            # 创建或获取 worktree
            worktree_path = self.create_worktree(version_config)
            if not worktree_path:
                print(f"[ERROR] 无法为版本 {version_config.display_name} 创建 worktree")
                continue
            
            try:
                # 构建文档
                if self.build_docs_in_worktree(worktree_path, version_config):
                    # 复制构建结果
                    if self.copy_build_result(worktree_path, version_config):
                        success_count += 1
                        print(f"[OK] 版本 {version_config.display_name} 构建成功")
                    else:
                        print(f"[ERROR] 版本 {version_config.display_name} 复制失败")
                else:
                    print(f"[ERROR] 版本 {version_config.display_name} 构建失败")
            finally:
                # 清理 worktree
                self.cleanup_worktree(worktree_path)
        
        # 创建统一入口页面，指向新的根目录结构
        self.create_unified_index()
        # 在 html 根目录下创建 index.html 指向默认版本
        self.create_versions_root_index()
        
        print("\n" + "=" * 60)
        print(f"构建完成: {success_count}/{total_count} 个版本成功")
        print("=" * 60)
        
        return success_count == total_count
    
    def create_unified_index(self):
        """创建统一的文档入口页面"""
        config = self.load_versions_config()
        versions = config.get('versions', [])
        default_version = config.get('default_version', '')
        latest_version = config.get('latest_version', '')
        
        # 找到默认版本的 URL 路径
        default_url = 'latest'
        for version in versions:
            if version['name'] == default_version:
                default_url = version['url_path']
                break
        
        # 创建根目录的 index.html
        index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SDK 文档</title>
    <meta http-equiv="refresh" content="0; url=./{default_url}/index.html">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .container {{
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }}
        .spinner {{
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        h1 {{
            margin: 0 0 10px 0;
            font-size: 24px;
        }}
        p {{
            margin: 0;
            opacity: 0.9;
        }}
        a {{
            color: white;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h1>SDK 文档</h1>
        <p>正在跳转到文档首页...</p>
        <p><a href="./{default_url}/index.html">如果页面没有自动跳转，请点击这里</a></p>
    </div>
</body>
</html>"""
        
        index_file = self.build_root / 'html' / 'index.html'
        index_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)
        
        print(f"[OK] 创建统一入口页面: {index_file}")

    def create_versions_root_index(self):
        """在versions目录下创建根页面"""
        config = self.load_versions_config()
        versions = config.get('versions', [])
        default_version = config.get('default_version', '')
        latest_version = config.get('latest_version', '')
        
        # 找到默认版本的 URL 路径
        default_url = 'latest'
        for version in versions:
            if version['name'] == default_version:
                default_url = version['url_path']
                break
        
        # 创建versions目录的index.html
        versions_index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SDK 文档 - 版本列表</title>
    <meta http-equiv="refresh" content="0; url=./{default_url}/index.html">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .container {{
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }}
        .spinner {{
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        h1 {{
            margin: 0 0 10px 0;
            font-size: 24px;
        }}
        p {{
            margin: 0;
            opacity: 0.9;
        }}
        a {{
            color: white;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h1>SDK 文档 - 版本列表</h1>
        <p>正在跳转到文档首页...</p>
        <p><a href="./{default_url}/index.html">如果页面没有自动跳转，请点击这里</a></p>
    </div>
</body>
</html>"""
        
        versions_index_file = self.versions_dir / 'index.html'
        versions_index_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(versions_index_file, 'w', encoding='utf-8') as f:
            f.write(versions_index_html)
        
        print(f"[OK] 创建versions目录根页面: {versions_index_file}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="中央构建管理器")
    parser.add_argument('--clean', action='store_true', help='清理构建目录')
    parser.add_argument('--list-versions', action='store_true', help='列出所有版本')
    parser.add_argument('--check-config', action='store_true', help='检查版本配置')
    
    args = parser.parse_args()
    
    try:
        manager = BuildManager()
        
        if args.list_versions:
            versions = manager.get_version_configs()
            print("版本列表:")
            for version in versions:
                print(f"  - {version.display_name} ({version.name}) -> {version.branch}")
            return
        
        if args.check_config:
            config = manager.load_versions_config()
            print("版本配置检查:")
            print(f"  默认版本: {config.get('default_version', 'N/A')}")
            print(f"  最新版本: {config.get('latest_version', 'N/A')}")
            print(f"  版本数量: {len(config.get('versions', []))}")
            return
        
        # 构建所有版本
        success = manager.build_all_versions(clean=args.clean)
        
        if success:
            print("\n[OK] 所有版本构建成功!")
            print(f"[PATH] 文档位置: {manager.versions_dir}")
        else:
            print("\n[ERROR] 部分版本构建失败!")
            sys.exit(1)
            
    except Exception as e:
        print(f"[ERROR] 构建管理器错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
