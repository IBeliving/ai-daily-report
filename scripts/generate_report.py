#!/usr/bin/env python3
"""
使用 AI 处理和总结新闻数据
"""
import os
import json
import requests
from pathlib import Path
from datetime import datetime

def get_ai_summary(content: str, max_length: int = 150) -> str:
    """使用 AI API 生成摘要"""
    
    # 检查是否有 OpenAI API Key
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        # 如果没有 API Key，使用简单摘要
        return content[:max_length] + "..." if len(content) > max_length else content
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个新闻摘要专家。请将以下内容用简洁的语言总结成一段话，不超过150字。保持客观，突出关键信息。"
                    },
                    {
                        "role": "user",
                        "content": content[:2000]  # 限制输入长度
                    }
                ],
                "temperature": 0.5,
                "max_tokens": 200
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        
    except Exception as e:
        print(f"AI 摘要生成失败: {e}")
    
    # Fallback: 截取前 N 个字符
    return content[:max_length] + "..." if len(content) > max_length else content

def process_articles():
    """处理并生成日报内容"""
    
    # 读取原始数据
    data_path = Path(__file__).parent.parent / "output" / "raw_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    report = {
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "generated_at": datetime.now().isoformat(),
        "sections": []
    }
    
    # 处理每个主题
    for topic_name, articles in data.get("raw_results", {}).items():
        if not articles:
            continue
        
        print(f"正在处理主题: {topic_name}")
        
        # 按分数排序，取前 5 条
        sorted_articles = sorted(articles, key=lambda x: x.get("score", 0), reverse=True)[:5]
        
        section = {
            "title": topic_name,
            "articles": []
        }
        
        for article in sorted_articles:
            # 生成 AI 摘要 (如果有 API Key)
            summary = get_ai_summary(article.get("content", ""))
            
            section["articles"].append({
                "title": article.get("title"),
                "url": article.get("url"),
                "summary": summary,
                "source": article.get("source", "未知来源")
            })
        
        report["sections"].append(section)
    
    # 保存处理后的报告数据
    report_path = Path(__file__).parent.parent / "output" / "report_data.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"报告数据生成完成，已保存到 {report_path}")
    return report

if __name__ == "__main__":
    process_articles()
