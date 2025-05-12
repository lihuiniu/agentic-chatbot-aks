from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from app.vector_store.faiss_store import FAISSVectorStore
from app.agents.cosmos_context import get_user_context
from langsmith import traceable

@traceable(name="ask_agent_with_context")
def ask_agent(question: str, user_id: str):
    context = get_user_context(user_id)
    store = FAISSVectorStore()
    retriever = FAISS(docs=[], embedding_function=lambda x: [0.0] * 1536).as_retriever()
    
    prompt = PromptTemplate.from_template(
        "You are a helpful assistant. Answer the question based on user context: {context} and vector docs. Q: {question}"
    )
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, chain_type_kwargs={"prompt": prompt})
    return qa.run({"context": context, "question": question})