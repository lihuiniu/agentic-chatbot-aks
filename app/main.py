from fastapi import FastAPI,Query
from app.teams_bot.webhook import router as teams_router
from pydantic import BaseModel
import cohere
import os

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.documents import Document

# --- ENV KEYS ---
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
cohere_api_key = "your-cohere-api-key"
co = cohere.Client(cohere_api_key)

app = FastAPI(title="Agentic Chatbot for Teams")

app.include_router(teams_router, prefix="/teams")

# --- Load & Index Data ---
loader = TextLoader("data/example_docs.txt")
raw_docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(raw_docs)

embedding_model = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})


# --- Hybrid RAG Logic ---
def hybrid_rerank(query: str, alpha=0.5, top_k=3):
    docs = retriever.get_relevant_documents(query)
    doc_texts = [doc.page_content for doc in docs]

    # Vector scores
    query_vector = embedding_model.embed_query(query)
    doc_vectors = [embedding_model.embed_query(doc.page_content) for doc in docs]

    def cosine_similarity(a, b):
        return sum(x * y for x, y in zip(a, b)) / (
                (sum(x**2 for x in a) ** 0.5) * (sum(y**2 for y in b) ** 0.5)
        )

    vector_scores = [cosine_similarity(query_vector, vec) for vec in doc_vectors]

    # Cohere rerank
    rerank_resp = co.rerank(query=query, documents=doc_texts, top_n=len(docs))
    cohere_scores = [0] * len(docs)
    for r in rerank_resp.results:
        cohere_scores[r.index] = r.relevance_score

    hybrid_docs = []
    for i in range(len(docs)):
        hybrid_score = alpha * cohere_scores[i] + (1 - alpha) * vector_scores[i]
        hybrid_docs.append({
            "content": docs[i].page_content,
            "vector_score": vector_scores[i],
            "cohere_score": cohere_scores[i],
            "hybrid_score": hybrid_score
        })

    # Sort by hybrid score
    hybrid_docs.sort(key=lambda d: d["hybrid_score"], reverse=True)
    return hybrid_docs[:top_k]


# --- Request Model ---
class QueryRequest(BaseModel):
    query: str
    alpha: float = 0.5
    top_k: int = 3

@app.get("/")
def health_check():
    return {"status": "running"}

# --- Endpoint ---
@app.post("/rag/search")
def rag_search(request: QueryRequest):
    results = hybrid_rerank(
        query=request.query,
        alpha=request.alpha,
        top_k=request.top_k
    )
    return {"query": request.query, "results": results}