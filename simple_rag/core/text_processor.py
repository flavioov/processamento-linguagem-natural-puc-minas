"""Processamento e divisão de textos."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from simple_rag.config import config
from simple_rag.logger import setup_logger

logger = setup_logger(__name__)


def split_documents(
    docs: list[Document],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[Document]:
    """Divide documentos em chunks menores.

    Args:
        docs: Lista de documentos para dividir
        chunk_size: Tamanho do chunk. Se None, usa config.chunk_size
        chunk_overlap: Overlap entre chunks. Se None, usa config.chunk_overlap

    Returns:
        Lista de documentos divididos em chunks
    """
    chunk_size = chunk_size or config.chunk_size
    chunk_overlap = chunk_overlap or config.chunk_overlap

    logger.info(f"Dividindo {len(docs)} documentos em chunks")
    logger.debug(f"Chunk size: {chunk_size}, Overlap: {chunk_overlap}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    all_splits = text_splitter.split_documents(docs)

    logger.info(f"Total de chunks criados: {len(all_splits)}")

    return all_splits


if __name__ == "__main__":
    from simple_rag.core.document_loader import load_documents

    docs = load_documents()
    split_docs = split_documents(docs)
    print(f"Documentos: {len(docs)}")
    print(f"Chunks: {len(split_docs)}")
