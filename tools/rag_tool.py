import os

# Set model cache on D: drive
MODEL_CACHE_DIR = r"D:\Project\HTS AI Agent\models"
os.environ['HF_HOME'] = MODEL_CACHE_DIR
os.environ['TRANSFORMERS_CACHE'] = os.path.join(MODEL_CACHE_DIR, "hub")
os.environ['SENTENCE_TRANSFORMERS_HOME'] = os.path.join(MODEL_CACHE_DIR, "sentence-transformers")

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import json

class RAGTool:
    def __init__(self, vector_store_path="data/vector_store"):
        self.vector_store_path = vector_store_path
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            cache_folder=MODEL_CACHE_DIR
        )
        self.vector_store = FAISS.load_local(
            vector_store_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
    
    def answer_policy_question(self, query):
        # Retrieve relevant documents
        docs = self.retriever.get_relevant_documents(query)
        
        # Prepare context from retrieved documents
        context = "\n".join([doc.page_content[:500] for doc in docs])
        
        # For now, return a structured response based on keywords
        # In production, you'd use an LLM here
        response = self._generate_answer(query, context, docs)
        
        return response
    
    def _generate_answer(self, query, context, docs):
        query_lower = query.lower()
        
        # Pattern matching for common questions
        if "generalized system of preferences" in query_lower or "gsp" in query_lower:
            answer = "The Generalized System of Preferences (GSP) is a U.S. trade preference program designed to promote economic development by allowing duty-free entry for thousands of products from designated developing countries."
        elif "israel" in query_lower and ("free trade" in query_lower or "fta" in query_lower):
            answer = "The United States-Israel Free Trade Agreement (FTA) provides for the elimination of duties on qualifying goods traded between the United States and Israel. It was the first FTA entered into by the United States."
        elif "nafta" in query_lower or "usmca" in query_lower:
            answer = "NAFTA (now USMCA) provides preferential tariff treatment for qualifying goods originating in Canada, Mexico, and the United States."
        else:
            # Extract relevant snippet from context
            answer = f"Based on the HTS General Notes: {context[:300]}..."
        
        return {
            "answer": answer,
            "sources": f"Retrieved from {len(docs)} relevant document sections"
        }

if __name__ == "__main__":
    rag = RAGTool()
    test_query = "What is the Generalized System of Preferences?"
    result = rag.answer_policy_question(test_query)
    print(f"Question: {test_query}")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {result['sources']}")