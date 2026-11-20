import chromadb


class KnowledgeBase:
    def __init__(self, path="./chroma_db", collection_name="pdt_tandil"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
    def add_knowledge(self, knowledge_id, knowledge_text, metadata=None):
        """Guarda textos con sus identificadores en la base vectorial."""
        self.collection.add(
            documents=[knowledge_text],
            ids=[knowledge_id],
            metadatas=[metadata] if metadata else [{}]
        )
    
    def search_knowledge(self, query: str, n_results: int = 2):
        """Busca textos similares en la base vectorial."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        docs = results['documents'][0] 
        return "\n".join(docs)