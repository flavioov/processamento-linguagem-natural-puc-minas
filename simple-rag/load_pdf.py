import pathlib
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf(file_path: pathlib.Path = "/data") -> List[Document]:
    """Load PDF(s) from a file or a directory.

    - loads all PDFs within it (recursively).
    """

    all_docs: List[Document] = []
    for pdf_path in file_path.rglob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        all_docs.extend(loader.load())
    return all_docs

def split(docs: list[Document], chuck_size: int = 1000, chuck_overlap: int = 200) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chuck_size, chunk_overlap=chuck_overlap)
    all_splits = text_splitter.split_documents(docs)
    return all_splits

if __name__ == "__main__":
    # You can pass a single PDF file or a directory containing PDFs
    docs = load_pdf()
    split_docs = split(docs)
    print(docs[0].page_content)
    print(len(docs))
    print(len(split_docs))
