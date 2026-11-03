import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class KnowledgeBase:
    def __init__(self):
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection("competitor_knowledge")
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    def ask(self, question):
        return {"answer": "test answer"}
