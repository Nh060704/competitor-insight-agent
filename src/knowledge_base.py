import chromadb
from chromadb.config import Settings

class KnowledgeBase:
    def __init__(self):
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection("competitor_knowledge")

    def add_documents(self, docs):
        self.collection.add(ids=["1"], documents=["test"])
