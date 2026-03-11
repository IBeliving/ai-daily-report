# AI Daily Report | AI 每日速递

> 每天自动采集AI与科技领域的最新资讯，生成精美的静态日报网站，并通过GitHub Pages自动发布。

![GitHub Actions](https://github.com/yourname/ai-daily-report/actions/workflows/daily-report.yml/badge.svg)

## 🌟 特性

- **定时自动化** - 每天上午8点（北京时间）自动运行
- **智能采集** - 基于 Tavily AI 搜索 API，精准获取最新资讯
- **AI 摘要** - 自动总结新闻内容（需配置 OpenAI API）
- **精美网页** - 响应式设计，Tailwind CSS 美化
- **零成本托管** - GitHub Actions + GitHub Pages 完全免费

## 🚀 快速开始

### 1. 部署到 GitHub Pages

```bash
# 克隆仓库
git clone https://github.com/yourname/ai-daily-report.git
cd ai-daily-report

# 安装依赖
pip install requests jinja2 pyyaml

# 测试运行
python scripts/fetch_news.py
python scripts/generate_report.py
python scripts/build_site.py
```

### 2. 配置 Secrets

在 GitHub 仓库的 **Settings → Secrets and variables → Actions** 中添加：

| Secret | 说明 | 获取方式 |
|--------|------|---------|
| `TAVILY_API_KEY` | Tavily API 密钥 | [tavily.com](https://tavily.com) |
| `OPENAI_API_KEY` | OpenAI API 密钥（可选） | [platform.openai.com](https://platform.openai.com) |

### 3. 配置关注领域

编辑 `config/topics.yml`，自定义你关注的领域和搜索关键词。

## 📁 项目结构

```
ai-daily-report/
├── .github/workflows/     # GitHub Actions 工作流
├── config/               # 配置文件
├── scripts/              # Python 脚本
│   ├── fetch_news.py     # 数据采集
│   ├── generate_report.py # AI 生成报告
│   └── build_site.py     # 构建静态网站
├── templates/            # Jinja2 模板
├── output/             # 生成的网站（gh-pages 分支）
└── README.md
```

## 🔄 工作流程

```
Cron: 每天8点 → GitHub Actions → 
  ├─ 采集新闻 (Tavily API)
  ├─ AI 处理 (OpenAI API / 本地)
  ├─ 生成网站 (Jinja2 → HTML)
  └─ 部署网站 (GitHub Pages)
```

## 📝 配置说明

### config/topics.yml

```yaml
topics:
  - name: "AI科技"
    keywords:
      - "AI人工智能最新进展"
      - "ChatGPT GPT-5"
    max_results: 5

tavily_config:
  topic: "news"
  days: 1
  search_depth: "advanced"
```

## 🛠️ 手动触发

访问仓库的 **Actions → Daily Report → Run workflow** 手动运行。

## 📄 许可证

MIT License
