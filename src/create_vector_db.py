from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_classic.schema import Document

def create_vector_db(text,embedder):
    doc=Document(page_content=text)
    splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100,separators=["\n\n","\n","."," "])

    docs=splitter.split_documents([doc])

    vectordb=FAISS.from_documents(docs,embedding=embedder)

    vectordb.save_local("research_paper_vector_db")

    return vectordb