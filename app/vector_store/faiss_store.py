import faiss
import numpy as np

class FAISSVectorStore:
    def __init__(self, dim=1536):
        self.index = faiss.IndexFlatL2(dim)
    
    def add(self, vectors):
        self.index.add(np.array(vectors).astype('float32'))
    
    def search(self, vector, top_k=5):
        D, I = self.index.search(np.array([vector]).astype('float32'), top_k)
        return I[0]