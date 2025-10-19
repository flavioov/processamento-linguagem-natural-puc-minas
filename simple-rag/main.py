import pathlib
from vectorstore import get_vetorstore
from langchain_huggingface import HuggingFaceEmbeddings
from load_pdf import load_pdf, split
from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import chain

from langchain_ollama import OllamaEmbeddings

from ollama_agent import agent
from langchain.tools import tool

def init_vectorstore():
    embedding_model = OllamaEmbeddings(model="llama3")
    vectorestore = get_vetorstore(embbedings_model=embedding_model)

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
    # agent
    # init vectorstore

    agent = agent()
    vectorestore = init_vectorstore()

    print("Enter 'exit' to exit")

    while True:
        query = input("Enter a query: ")
        if query == "exit":
            print("Exiting...")
            break

        retriever = vectorestore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3},
        )
        output = retriever.invoke(input=query)

        for doc in output:
            file_content = doc.page_content
            print(f"Page {doc.metadata['page']}:\n{file_content}\n")