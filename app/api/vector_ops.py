from fastapi import APIRouter, HTTPException
from app.vector_store.faiss_store import FAISSVectorStore
from app.embeddings.openai_embedder import embed_text

router = APIRouter()

@router.post("/vector/update")
def update_vector(doc_id: str, content: str):
    store = FAISSVectorStore()
    embedding = embed_text(content)
    if not store.update_by_id(doc_id, embedding):
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "updated", "doc_id": doc_id}