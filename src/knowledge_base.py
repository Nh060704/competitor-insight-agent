"""
RAG 知识库模块
负责文档切片、向量存储、语义检索和 LLM 回答生成
"""
import chromadb
from chromadb.config import Settings
from openai import OpenAI
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class KnowledgeBase:
    def __init__(self, collection_name: str = None, persist_dir: str = None):
        # 持久化存储，重启不丢失
        self.persist_dir = persist_dir or os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )

        self.collection_name = collection_name or os.getenv("COLLECTION_NAME", "competitor_knowledge")
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

        # 初始化 OpenAI 客户端（模型可通过环境变量配置）
        self.model_name = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.llm_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )

    def add_documents(self, documents: List[Dict]):
        """添加文档到知识库"""
        ids = []
        texts = []
        metadatas = []

        for doc in documents:
            if doc["status"] != "success" or not doc["content"]:
                continue

            chunks = self._split_text(doc["content"])
            for j, chunk in enumerate(chunks):
                ids.append(f"{doc['url']}_{j}")
                texts.append(chunk)
                metadatas.append({
                    "url": doc["url"],
                    "title": doc["title"],
                    "chunk_index": j
                })

        if texts:
            self.collection.add(ids=ids, documents=texts, metadatas=metadatas)
            print(f"已添加 {len(texts)} 个文档切片到知识库")

    def _split_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """文本切片：按固定长度切分，保留一定重叠"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        return chunks

    def query(self, question: str, n_results: int = 3) -> Dict:
        """语义检索相关文档片段"""
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )
        return results

    def ask(self, question: str, n_results: int = 3) -> Dict:
        """RAG 完整流程：检索 + 生成回答"""
        try:
            # 1. 检索相关片段
            search_results = self.query(question, n_results=n_results)
            relevant_docs = search_results["documents"][0] if search_results["documents"] else []
            sources = search_results["metadatas"][0] if search_results["metadatas"] else []

            if not relevant_docs:
                return {
                    "question": question,
                    "answer": "知识库中没有找到相关信息，请先采集竞品数据。",
                    "sources": []
                }

            # 2. 拼 prompt，调用 LLM 生成回答
            context = "\n\n".join([f"[片段{i+1}] {doc}" for i, doc in enumerate(relevant_docs)])

            prompt = f"""你是一个竞品分析助手。请根据下面提供的参考资料，回答用户的问题。
如果参考资料中没有相关信息，请明确说明"资料中未提及"，不要编造。

参考资料：
{context}

用户问题：{question}

请用简洁的中文回答，并在末尾标注信息来源。"""

            response = self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )

            answer = response.choices[0].message.content

            return {
                "question": question,
                "answer": answer,
                "sources": [s["url"] for s in sources]
            }
        except Exception as e:
            return {
                "question": question,
                "answer": f"调用大模型失败: {str(e)}",
                "sources": []
            }

    def get_stats(self) -> Dict:
        """获取知识库统计信息"""
        count = self.collection.count()
        return {
            "total_chunks": count,
            "collection_name": self.collection_name,
            "persist_dir": self.persist_dir
        }


if __name__ == "__main__":
    kb = KnowledgeBase()
    print(f"知识库统计: {kb.get_stats()}")
