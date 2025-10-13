import pathlib
from embedding import get_vetorstore
from langchain_huggingface import HuggingFaceEmbeddings
from load_pdf import load_pdf, split
from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import chain

@chain
def _retriever(query: str, vectorstore) -> List[Document]:
    return vectorstore.similarity_search(query, k=1)

if __name__ == "__main__":
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorestore = get_vetorstore(embbedings_model=embedding_model)
    file_path = pathlib.Path("../data/chapter-6-embedding.pdf")

    print("loading the pdf")

    docs = load_pdf(file_path=file_path)
    print("splitting the pdf")

    split_docs = split(docs)
    print("Adding the documents to the vectorstore")

    ids = vectorestore.add_documents(documents=split_docs)
    print(f"Added {len(ids)} documents to the vectorstore")
    print(f"Ids:\n{ids}")
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