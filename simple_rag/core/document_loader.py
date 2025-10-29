"""Carregamento de documentos de várias fontes."""

import pathlib

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

from simple_rag.config import config
from simple_rag.logger import setup_logger

logger = setup_logger(__name__)


def load_documents(data_dir: pathlib.Path | None = None) -> list[Document]:
    """Carrega todos os arquivos .txt recursivamente de um diretório.

    Args:
        data_dir: Diretório contendo os documentos.
                  Se None, usa config.get_data_dir()

    Returns:
        Lista de documentos carregados

    Raises:
        FileNotFoundError: Se o diretório não existe
    """
    path = data_dir or config.get_data_dir()

    if not path.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {path}")

    logger.info(f"Carregando documentos de: {path}")

    # Coleta todos os arquivos .txt recursivamente
    all_paths = [p for p in path.rglob("*.txt") if p.is_file()]

    logger.info(f"Encontrados {len(all_paths)} arquivos .txt")

    all_docs: list[Document] = []
    errors = []

    for file_path in all_paths:
        try:
            loader = TextLoader(str(file_path), encoding="utf-8")
            docs = loader.load()
            all_docs.extend(docs)
            logger.debug(f"✓ Carregado: {file_path.name}")
        except Exception as e:
            errors.append((file_path, e))
            logger.warning(f"✗ Erro ao carregar {file_path.name}: {e}")

    if errors:
        logger.warning(f"Falha ao carregar {len(errors)} arquivo(s)")

    logger.info(f"Total de documentos carregados: {len(all_docs)}")

    return all_docs


if __name__ == "__main__":
    docs = load_documents()
    print(f"Documentos carregados: {len(docs)}")
