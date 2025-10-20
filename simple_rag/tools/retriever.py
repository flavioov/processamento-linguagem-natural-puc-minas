"""
Ferramenta de recuperação de documentos.
"""
from typing import List
from langchain.tools import tool
from langchain_core.documents import Document

from simple_rag.core.vectorstore import get_vectorstore
from simple_rag.config import config
from simple_rag.logger import setup_logger

logger = setup_logger(__name__)

# Inicializar vectorstore globalmente (lazy loading)
_vectorstore = get_vectorstore()

def _get_vectorstore():
    """Retorna vectorstore (singleton)."""
    global _vectorstore
    if _vectorstore is None:
        logger.info("Inicializando vectorstore...")
        _vectorstore = get_vectorstore()
    return _vectorstore

@tool
def retriever(query: str) -> List[Document]:
    """
    Busca documentos relevantes no vectorstore.

    Args:
        query: Consulta de busca

    Returns:
        Lista de documentos relevantes
    """
    logger.debug(f"Buscando documentos para query: '{query}'")

    vectorstore = _get_vectorstore()

    retriever_instance = vectorstore.as_retriever(
        search_type=config.RETRIEVAL_TYPE,
        search_kwargs={"k": config.RETRIEVAL_K},
    )

    results = retriever_instance.invoke(input=query)

    logger.debug(f"Encontrados {len(results)} documentos relevantes")

    return results
