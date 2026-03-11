#!/usr/bin/env python3
"""
采集新闻数据 - 通过 Tavily API
"""
import os
import sys
import json
import requests
import yaml
from pathlib import Path

def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config" / "topics.yml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def search_tavily(query: str, topic: str = "general", days: int = 1, 
                  max_results: int = 5, search_depth: str = "basic"):
    """调用 Tavily API 搜索"""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        # 尝试从配置文件读取 (开发环境)
        try:
            with open(Path(__file__).parent.parent / ".env", "r") as f:
                for line in f:
                    if line.startswith("TAVILY_API_KEY="):
                        api_key = line.strip().split("=", 1)[1]
                        break
        except:
            pass
    
    if not api_key:
        print("错误: 未设置 TAVILY_API_KEY")
        sys.exit(1)
    
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": search_depth,
        "topic": topic,
        "max_results": min(max_results, 20),
        "include_answer": True,
        "include_raw_content": False,
    }
    
    if topic == "news" and days:
        payload["days"] = days
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"搜索失败: {query}, 错误: {e}")
        return {"results": [], "answer": ""}

def fetch_all_topics():
    """采集所有关注领域的新闻"""
    config = load_config()
    all_data = {
        "generated_at": None,
        "topics": [],
        "raw_results": {}
    }
    
    tavily_cfg = config.get("tavily_config", {})
    
    for topic_cfg in config.get("topics", []):
        topic_name = topic_cfg["name"]
        keywords = topic_cfg.get("keywords", [])
        max_results = topic_cfg.get("max_results", 5)
        
        print(f"正在采集: {topic_name}")
        
        topic_data = {
            "name": topic_name,
            "articles": []
        }
        
        # 对每个关键词搜索
        for keyword in keywords:
            print(f"  搜索: {keyword}")
            result = search_tavily(
                query=keyword,
                topic=tavily_cfg.get("topic", "news"),
                days=tavily_cfg.get("days", 1),
                max_results=max_results,
                search_depth=tavily_cfg.get("search_depth", "advanced")
            )
            
            # 存储原始结果用于AI处理
            if topic_name not in all_data["raw_results"]:
                all_data["raw_results"][topic_name] = []
            
            for article in result.get("results", []):
                all_data["raw_results"][topic_name].append({
                    "title": article.get("title"),
                    "url": article.get("url"),
                    "content": article.get("content"),
                    "published_date": article.get("published_date"),
                    "source": article.get("source"),
                    "score": article.get("score")
                })
                
                topic_data["articles"].append({
                    "title": article.get("title"),
                    "url": article.get("url"),
                    "summary": article.get("content", "")[:300] + "..." if len(article.get("content", "")) > 300 else article.get("content", "")
                })
        
        all_data["topics"].append(topic_data)
    
    # 保存原始数据
    output_path = Path(__file__).parent.parent / "output" / "raw_data.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"数据采集完成，已保存到 {output_path}")
    return all_data

if __name__ == "__main__":
    from datetime import datetime
    data = fetch_all_topics()
    data["generated_at"] = datetime.now().isoformat()
    
    # 更新保存
    output_path = Path(__file__).parent.parent / "output" / "raw_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
