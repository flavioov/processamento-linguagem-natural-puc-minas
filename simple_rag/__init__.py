"""Simple RAG - Sistema de Recuperação e Geração Aumentada.

Um sistema RAG (Retrieval-Augmented Generation) que utiliza LangChain,
Ollama e LangGraph para criar um agente conversacional com acesso a
documentos médicos.
"""

__version__ = "0.1.0"

from simple_rag.config import config
from simple_rag.utils.logger import setup_logger

__all__ = ["config", "setup_logger"]
