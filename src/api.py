"""
FastAPI 接口模块
提供竞品采集、知识库查询和智能问答的 API
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from .knowledge_base import KnowledgeBase
from .collector import WebCollector
import uvicorn

app = FastAPI(title="Competitor Insight Agent API", version="0.2.0")
kb = KnowledgeBase()


class CollectRequest(BaseModel):
    url: str


class AskRequest(BaseModel):
    question: str
    top_k: int = 3


@app.get("/")
def root():
    return {"message": "Competitor Insight Agent API", "version": "0.2.0"}


@app.get("/api/stats")
def get_stats():
    """获取知识库统计信息"""
    return kb.get_stats()


@app.post("/api/collect")
def collect_website(req: CollectRequest):
    """采集指定网站的关键页面并存入知识库"""
    collector = WebCollector(req.url)
    results = collector.collect_common_pages()
    kb.add_documents(results)
    return {
        "message": "采集完成",
        "pages_collected": len([r for r in results if r["status"] == "success"]),
        "results": results
    }


@app.post("/api/ask")
def ask_question(req: AskRequest):
    """RAG 智能问答：根据知识库内容回答问题"""
    result = kb.ask(req.question, n_results=req.top_k)
    return result


def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start_server()
