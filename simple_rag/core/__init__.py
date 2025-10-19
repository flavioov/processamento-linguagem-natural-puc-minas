"""
Módulos principais do sistema RAG.
"""
from simple_rag.core.document_loader import load_documents
from simple_rag.core.text_processor import split_documents
from simple_rag.core.vectorstore import get_vectorstore, init_vectorstore

__all__ = [
    "load_documents",
    "split_documents",
    "get_vectorstore",
    "init_vectorstore"
]
