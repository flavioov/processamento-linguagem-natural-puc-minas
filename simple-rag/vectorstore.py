import pathlib
from langchain_core.vectorstores import InMemoryVectorStore

from langchain_huggingface import HuggingFaceEmbeddings
from load_pdf import load_pdf, split
from langchain_ollama import OllamaEmbeddings

def init_vetorstore(embbedings_model: OllamaEmbeddings, ):
    return InMemoryVectorStore(embbedings_model)

def get_vectorstore():
    embedding_model = OllamaEmbeddings(model="llama3")
    vectorestore = init_vetorstore(embbedings_model=embedding_model)

    print("loading the pdf")

    docs = load_pdf()
    print("splitting the pdf")

    split_docs = split(docs)
    print("Adding the documents to the vectorstore")

    ids = vectorestore.add_documents(documents=split_docs)
    print(f"Added {len(ids)} documents to the vectorstore")
    print(f"Ids:\n{ids}")

    return vectorestore

if __name__ == "__main__":
    vectorestore = get_vectorstore()

    results = vectorestore.as_retriever("what is the focus of this chapter", k=5)

    doc, score = results[0]
    print(f"Score: {score}\n")
    print(doc)
    print(doc.page_content)