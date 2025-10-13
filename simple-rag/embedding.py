import pathlib
from langchain_core.vectorstores import InMemoryVectorStore

from langchain_huggingface import HuggingFaceEmbeddings
from load_pdf import load_pdf, split

def get_vetorstore(embbedings_model: HuggingFaceEmbeddings, ):
    return InMemoryVectorStore(embbedings_model)

if __name__ == "__main__":
    file_path = pathlib.Path("../data/chapter-6-embedding.pdf")
    print("loading the pdf")
    docs = load_pdf(file_path=file_path)
    print("splitting the pdf")
    split_docs = split(docs)

    # https://huggingface.co/sentence-transformers/all-mpnet-base-v2
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorestore = get_vetorstore(embeddings)

    ids = vectorestore.add_documents(documents=split_docs)
    print(f"Added {len(ids)} documents to the vectorstore")
    print(f"Ids:\n{ids}")

    # results = vectorestore.similarity_search(
    #     "what is the focus of this chapter ?"
    # )
    results = vectorestore.similarity_search_with_score("what is the focus of this chapter", k=5)

    doc, score = results[0]
    print(f"Score: {score}\n")
    print(doc)
    print(doc.page_content)