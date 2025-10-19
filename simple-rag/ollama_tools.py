from typing import List, Optional, Dict

from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.runnables import chain
from langchain_ollama import OllamaEmbeddings
from vectorstore import get_vectorstore

vectorstore = get_vectorstore()


@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


@chain
def _retriever(query: str, vectorstore) -> List[Document]:
    return vectorstore.similarity_search(query, k=1)


def retriever(query: str, search_type="similarity", search_kwargs: Optional[Dict] = {"k": 4}) -> list[Document]:
    """Return List of relevant documents from vectorstore.

    Args:
        query: The query string.
        search_type (Optional[str]): Defines the type of search that
            the Retriever should perform.
            Can be "similarity" (default), "mmr", or
            "similarity_score_threshold".
        search_kwargs (Optional[Dict]): Keyword arguments to pass to the
            search function. Can include things like:
                k: Amount of documents to return (Default: 4)
                score_threshold: Minimum relevance threshold
                    for similarity_score_threshold
                fetch_k: Amount of documents to pass to MMR algorithm
                    (Default: 20)
                lambda_mult: Diversity of results returned by MMR;
                    1 for minimum diversity and 0 for maximum. (Default: 0.5)
                filter: Filter by document metadata
    Returns:
        List of relevant documents.

    """

    return (vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs)
            .invoke(input=query))
