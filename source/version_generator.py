#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本生成器
根据 .github/versions.json 文件生成不同版本的文档
支持多分支文档生成
"""

import os
import sys
import shutil
import subprocess
import yaml
from pathlib import Path

def load_versions():
    """从 versions.json 文件加载版本列表"""
    versions_file = Path("../.github/versions.json")
    if not versions_file.exists():
        print(f"错误: 版本文件不存在: {versions_file}")
        return []
    
    try:
        import json
        with open(versions_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        versions = list(config.get('versions', {}).keys())
        print(f"加载版本配置: {versions}")
        return versions
    except (json.JSONDecodeError, KeyError) as e:
        print(f"错误: 版本配置文件格式错误: {e}")
        return []

def get_main_branch():
    """从版本配置中获取主分支名称"""
    versions_file = Path("../.github/versions.json")
    if not versions_file.exists():
        return 'main'  # 默认值
    
    try:
        import json
        with open(versions_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 查找显示为"最新版本"的分支
        for version, display_name in config.get('versions', {}).items():
            if display_name == "最新版本":
                return version
        
        # 如果没有找到，返回第一个版本或默认值
        versions = list(config.get('versions', {}).keys())
        return versions[0] if versions else 'main'
    except (json.JSONDecodeError, KeyError):
        return 'main'  # 默认值

def get_branch_name():
    """获取当前分支名称"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("警告: 无法获取当前分支名称")
        return None

def check_branch_exists(branch_name):
    """检查分支是否存在（改进版本）"""
    try:
        # 首先检查本地分支
        result = subprocess.run(
            ['git', 'branch', '--list', branch_name],
            capture_output=True, text=True, check=True
        )
        if result.stdout.strip():
            return True
        
        # 检查远程分支（如果网络可用）
        try:
            result = subprocess.run(
                ['git', 'ls-remote', '--heads', 'origin', branch_name],
                capture_output=True, text=True, check=True, timeout=10
            )
            return bool(result.stdout.strip())
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print(f"警告: 无法检查远程分支 {branch_name}，假设存在")
            return True
            
    except subprocess.CalledProcessError:
        print(f"警告: 无法检查分支 {branch_name}，假设存在")
        return True

def checkout_branch(branch_name):
    """切换到指定分支"""
    try:
        print(f"切换到分支: {branch_name}")
        subprocess.run(['git', 'checkout', branch_name], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: 无法切换到分支 {branch_name}: {e}")
        return False

def get_branch_versions():
    """获取当前分支对应的版本列表"""
    current_branch = get_branch_name()
    if not current_branch:
        return []
    
    versions = load_versions()
    branch_versions = []
    
    for version in versions:
        # 检查版本是否对应当前分支
        if version == current_branch:
            branch_versions.append(version)
        elif version == 'main' and current_branch == 'main':
            # 处理主分支名称差异
            branch_versions.append(version)
        elif version == 'main' and current_branch == 'master':
            # 处理主分支名称差异（master -> main）
            branch_versions.append(version)
    
    print(f"当前分支 {current_branch} 对应的版本: {branch_versions}")
    return branch_versions

def build_version_docs(version, branch_name=None):
    """为指定版本构建文档"""
    print(f"\n开始构建版本 {version} 的文档...")
    
    # 确定对应的分支名称
    if branch_name is None:
        branch_name = version
    
    # 创建版本输出目录
    if version == 'main':
        output_dir = Path("_build/html/latest")
    else:
        output_dir = Path(f"_build/html/{version}")
    
    # 清理输出目录
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 检查是否在GitHub Actions环境中
        is_github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'
        
        # 保存当前分支名称
        current_branch = get_branch_name()
        print(f"当前分支: {current_branch}")
        
        # 如果需要切换到不同分支
        if branch_name != current_branch:
            print(f"切换到分支: {branch_name}")
            subprocess.run(['git', 'checkout', branch_name], check=True)
            
            # 拉取最新代码（仅在GitHub Actions中）
            if is_github_actions:
                try:
                    subprocess.run(['git', 'pull', 'origin', branch_name], check=True)
                except subprocess.CalledProcessError:
                    print(f"警告: 无法拉取分支 {branch_name} 的最新代码")
        else:
            print(f"已在目标分支: {branch_name}")
        
        # 运行文档生成脚本
        subprocess.run([
            sys.executable, 'doc_generator.py'
        ], cwd=".", check=True)
        
        # 构建HTML文档
        subprocess.run([
            sys.executable, '-m', 'sphinx.cmd.build',
            '-b', 'html',
            '.',
            str(output_dir)
        ], cwd=".", check=True)
        
        # 复制版本配置文件到构建目录
        source_versions = Path("../.github/versions.json")
        target_versions = output_dir / "_static" / "versions.json"
        if source_versions.exists():
            target_versions.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_versions, target_versions)
            print(f"✓ 版本配置文件已复制到: {target_versions}")
        
        # 如果切换了分支，恢复到原始分支
        if branch_name != current_branch:
            print(f"恢复到原始分支: {current_branch}")
            subprocess.run(['git', 'checkout', current_branch], check=True)
        
        print(f"✓ 版本 {version} 文档构建完成: {output_dir}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ 版本 {version} 文档构建失败: {e}")
        return False

def create_version_config():
    """从 .github/versions.json 复制版本配置到静态文件目录"""
    print("\n复制版本配置文件...")
    
    # 读取源配置文件
    source_config_file = Path("../.github/versions.json")
    if not source_config_file.exists():
        print(f"错误: 源版本配置文件不存在: {source_config_file}")
        return False
    
    try:
        import json
        with open(source_config_file, 'r', encoding='utf-8') as f:
            version_config = json.load(f)
        
        # 写入到静态文件目录
        config_file = Path("../.github/versions.json")
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(version_config, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 版本配置文件复制完成: {config_file}")
        return True
    except (json.JSONDecodeError, IOError) as e:
        print(f"错误: 复制版本配置文件失败: {e}")
        return False

def create_root_redirect():
    """创建根目录重定向页面"""
    print("\n创建根目录重定向页面...")
    
    # 创建根目录的 index.html，重定向到latest版本
    root_index = Path("_build/html/index.html")
    root_index.parent.mkdir(parents=True, exist_ok=True)
    
    redirect_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SDK 文档</title>
    <meta http-equiv="refresh" content="0; url=./latest/">
    <script>
        // 立即跳转到latest版本
        window.location.href = './latest/';
    </script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }
        .spinner {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        h1 {
            margin: 0 0 10px 0;
            font-size: 24px;
        }
        p {
            margin: 0;
            opacity: 0.9;
        }
        a {
            color: white;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h1>SDK 文档</h1>
        <p>正在跳转到最新版本...</p>
        <p><a href="./latest/">如果页面没有自动跳转，请点击这里</a></p>
    </div>
</body>
</html>"""
    
    with open(root_index, 'w', encoding='utf-8') as f:
        f.write(redirect_html)
    
    print(f"✓ 根目录重定向页面创建完成: {root_index}")
    return True

def main():
    """主函数"""
    print("开始生成多版本文档...")
    
    # 检查是否在GitHub Actions环境中
    is_github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'
    
    if is_github_actions:
        print("检测到GitHub Actions环境")
        # 在GitHub Actions中，为所有版本构建文档
        versions = load_versions()
        if not versions:
            print("错误: 没有找到有效的版本配置")
            return 1
        
        # 获取当前分支名称
        current_branch = get_branch_name()
        print(f"当前触发分支: {current_branch}")
        
        # 为每个版本构建文档
        results = {}
        for version in versions:
            # 检查分支是否存在
            if check_branch_exists(version):
                print(f"✓ 分支 {version} 存在，开始构建")
                success = build_version_docs(version, version)
            else:
                print(f"⚠️  分支 {version} 不存在，跳过构建")
                success = False
            results[version] = success
    else:
        print("本地构建环境")
        # 在本地环境中，可以选择构建所有版本或只构建当前分支对应的版本
        import sys
        build_all = len(sys.argv) > 1 and sys.argv[1] == '--all'
        
        if build_all:
            print("构建所有版本...")
            versions = load_versions()
            results = {}
            for version in versions:
                # 检查分支是否存在
                if check_branch_exists(version):
                    print(f"✓ 分支 {version} 存在，开始构建")
                    success = build_version_docs(version, version)
                else:
                    print(f"⚠️  分支 {version} 不存在，跳过构建")
                    success = False
                results[version] = success
        else:
            print("只构建当前分支对应的版本...")
            # 只构建当前分支对应的版本
            branch_versions = get_branch_versions()
            if not branch_versions:
                print("警告: 当前分支没有对应的版本配置")
                # 尝试构建默认版本
                branch_versions = ['main']
            
            results = {}
            for version in branch_versions:
                success = build_version_docs(version)
                results[version] = success
    
    # 输出结果
    print("\n" + "="*50)
    print("版本生成结果:")
    for version, success in results.items():
        status = "✓ 成功" if success else "✗ 失败"
        print(f"  {version}: {status}")
    
    success_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    print(f"\n总计: {success_count}/{total_count} 个版本生成成功")
    
    # 在所有版本构建完成后创建根目录重定向页面和版本配置
    if success_count > 0:
        create_version_config()
        create_root_redirect()
    
    if success_count == total_count:
        print("🎉 所有版本生成完成！")
        return 0
    else:
        print("⚠️  部分版本生成失败，请检查错误信息")
        return 1

if __name__ == "__main__":
    sys.exit(main())
