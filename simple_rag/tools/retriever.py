"""Ferramenta de recuperação de documentos."""

from langchain.tools import tool
from langchain_core.documents import Document

from simple_rag.config import config
from simple_rag.core.vectorstore import get_vectorstore
from simple_rag.logger import setup_logger

logger = setup_logger(__name__)


def _get_vectorstore():
    """Retorna vectorstore (singleton)."""
    _vectorstore = get_vectorstore()
    if _vectorstore is None:
        logger.info("Inicializando vectorstore...")
        _vectorstore = get_vectorstore()
    return _vectorstore


@tool
def retriever(query: str) -> list[Document]:
    """Busca documentos relevantes no vectorstore.

    Args:
        query: Consulta de busca

    Returns:
        Lista de documentos relevantes
    """
    logger.debug(f"Buscando documentos para query: '{query}'")

    vectorstore = _get_vectorstore()

    retriever_instance = vectorstore.as_retriever(
        search_type=config.retrieval_type,
        search_kwargs={"k": config.retrieval_k},
    )

    results: list[Document] = retriever_instance.invoke(input=query)

    logger.debug(f"Encontrados {len(results)} documentos relevantes")

    return results
