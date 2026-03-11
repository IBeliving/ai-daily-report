#!/usr/bin/env python3
"""
生成静态网站
"""
import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from jinja2 import Template

def ensure_output_dir():
    """确保输出目录存在"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制静态文件
    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.exists():
        for item in static_dir.iterdir():
            dest = output_dir / item.name
            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
    
    return output_dir

def get_html_template():
    """获取 HTML 模板"""
    template_path = Path(__file__).parent.parent / "templates" / "report.html.j2"
    
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    
    # 默认模板
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Daily Report - {{ date }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans SC', sans-serif; }
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card-hover { transition: all 0.3s ease; }
        .card-hover:hover { transform: translateY(-2px); box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <header class="gradient-bg text-white py-12">
        <div class="container mx-auto px-4 text-center">
            <h1 class="text-4xl md:text-5xl font-bold mb-3">AI 每日速递</h1>
            <p class="text-xl opacity-90">{{ subtitle }}</p>
            <p class="mt-4 text-sm opacity-75">{{ date }} 更新</p>
        </div>
    </header>
    
    <main class="container mx-auto px-4 py-8">
        {% for section in sections %}
        <section class="mb-12">
            <div class="flex items-center mb-6">
                <div class="w-1 h-8 bg-indigo-600 rounded mr-4"></div>
                <h2 class="text-2xl font-bold text-gray-800">{{ section.title }}</h2>
            </div>
            
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {% for article in section.articles %}
                <article class="bg-white rounded-xl shadow-md overflow-hidden card-hover">
                    <div class="p-6">
                        <h3 class="font-semibold text-lg text-gray-800 mb-3 line-clamp-2">
                            <a href="{{ article.url }}" target="_blank" class="hover:text-indigo-600 transition-colors">
                                {{ article.title }}
                            </a>
                        </h3>
                        <p class="text-gray-600 text-sm line-clamp-3 mb-4">{{ article.summary }}</p>
                        <div class="flex items-center justify-between text-xs text-gray-400">
                            <span class="flex items-center">📰 {{ article.source }}</span>
                            <a href="{{ article.url }}" target="_blank" class="text-indigo-600 hover:underline">阅读全文 →</a>
                        </div>
                    </div>
                </article>
                {% endfor %}
            </div>
        </section>
        {% endfor %}
    </main>
    
    <footer class="bg-gray-800 text-gray-400 py-6 mt-12">
        <div class="container mx-auto px-4 text-center">
            <p>AI Daily Report - 每日自动更新</p>
            <p class="text-sm mt-2">Generated at {{ generated_at }}</p>
            <p class="text-xs mt-2 opacity-50">
                数据来源: Tavily API · 
                <a href="https://github.com/{{ github_repo }}" target="_blank" class="hover:text-white transition-colors">GitHub</a>
            </p>
        </div>
    </footer>
</body>
</html>'''

def build_site():
    """构建网站"""
    output_dir = ensure_output_dir()
    
    # 读取报告数据
    report_path = Path(__file__).parent.parent / "output" / "report_data.json"
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
    
    # 加载配置
    config_path = Path(__file__).parent.parent / "config" / "topics.yml"
    import yaml
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # 准备模板变量
    template_vars = {
        "date": report.get("date", datetime.now().strftime("%Y年%m月%d日")),
        "generated_at": report.get("generated_at", ""),
        "subtitle": config.get("report_config", {}).get("subtitle", "精选 AI 与科技领域最新动态"),
        "sections": report.get("sections", []),
        "github_repo": os.environ.get("GITHUB_REPOSITORY", "yourname/ai-daily-report")
    }
    
    # 渲染模板
    template = Template(get_html_template())
    html = template.render(**template_vars)
    
    # 保存 HTML
    index_path = output_dir / "index.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"网站生成完成: {index_path}")
    return index_path

if __name__ == "__main__":
    build_site()
