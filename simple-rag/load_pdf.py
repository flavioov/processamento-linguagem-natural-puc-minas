import pathlib

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_pdf(file_path:pathlib.Path):
    loader = PyPDFLoader(file_path)
    docs =  loader.load()
    return docs

def split(docs: list[Document], chuck_size: int=1000, chuck_overlap: int=200) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chuck_size, chunk_overlap=chuck_overlap)
    all_splits = text_splitter.split_documents(docs)
    return all_splits

if __name__ == "__main__":
    file_path = pathlib.Path("../data/chapter-6-embedding.pdf")
    docs = load_pdf(file_path=file_path)
    split_docs = split(docs)
    print(docs[0].page_content)
    print(len(docs))
    print(len(split_docs))
