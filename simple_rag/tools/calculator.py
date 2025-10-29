"""Ferramentas de cálculo matemático."""

from langchain.tools import tool


@tool
def add(a: int, b: int) -> int:
    """Soma dois números inteiros.

    Args:
        a: Primeiro número
        b: Segundo número

    Returns:
        Soma de a e b
    """
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplica dois números inteiros.

    Args:
        a: Primeiro número
        b: Segundo número

    Returns:
        Produto de a e b
    """
    return a * b
