from langchain.vectorstores import FAISS
from langchain_cohere import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import cohere

# Initialize Cohere
co = cohere.Client("your-cohere-api-key")

# Load and split documents
docs = TextLoader("/data/product_docs.txt").load()
chunks = RecursiveCharacterTextSplitter(chunk_size= 500, chunk_overlap = 100).split_documents(docs)

# Embedding + vectorstore setup
embedding_model = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embedding_model)
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

#Cohere Reranker
cohere_reranker = CohereRerank(top_n = 3) # keep only top-3 reranked docs


# Wrap retriever with contextual compression
rerank_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    base_compressor=cohere_reranker
)

#  Combine Vector Similarity + Cohere Rerank (Hybrid Scoring)
# 0.3 favors Cohere semantic match, 0.7 favors vector similarity
def hybrid_score(query: str, retriever, embedding_model, alpha=0.3, top_k = 3):
    docs = retriever.get_relevant_documents(query)
    doc_texts = [doc.page_content for doc in docs]

    # vector similarity(cosine similarity)
    query_vector = embedding_model.embed_query(query)
    doc_vectors = [embedding_model.embed_query(doc.page_content) for doc in docs]

    def cosine_similarity(a, b):
        return sum(x * y for x, y in zip(a, b)) / ((sum(x ** 2 for x in a) ** 0.5) * (sum(y ** 2 for y in b) ** 0.5))

    vector_scores =[cosine_similarity(query_vector, vec) for vec in doc_vectors]

    #Cohere Rerank
    cohere_results = co.rerank(query = query, documents = doc_texts, top_n = len(docs))
    cohere_scores = [0] * len(docs)
    for result in cohere_results.results:
        cohere_scores[result.index] = result.relevance_score

    # Combine scores
    hybrid =[
        {
            "doc": docs[i],
            "vector_score": vector_scores[i],
            "cohere_score": cohere_scores[i],
            "hybrid_score": alpha * cohere_scores[i] + (1 - alpha) * vector_scores[i],
        }
        for i in range(len(docs))
    ]

    # Sort and return top_k
    top_docs = sorted(hybrid, key=lambda d: d["hybrid_score"], reverse=True)[:top_k]

   print("\n Hybrid reranked results: \n")
   for i, e in enumerate(top_docs):
       print(f"[#{i + 1}] Hybrid Score: {e['hybrid_score']: .3f} | Vector: {e['vector_Score']: .3f} | Cohere : {e['cohere_score']: .3f}")
       print(f"Snippet: {e['doc'].page_content[:200].replace('\n', ' ')}... \n")

    return [e["doc"] for e in top_docs]

    return [entry["doc"] for entry in top_docs]
