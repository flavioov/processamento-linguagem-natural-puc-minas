from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from simple_rag.config import config
from simple_rag.core.document_loader import load_documents
from simple_rag.core.text_processor import split_documents
from simple_rag.logger import setup_logger

logger = setup_logger(__name__)


def init_vectorstore(embeddings_model):
    """Inicializa um vectorstore em memória."""
    return InMemoryVectorStore(embeddings_model)


def get_vectorstore():
    """Cria e popula um vectorstore com os documentos.

    Returns:
        Vectorstore populado
    """
    logger.info("Criando embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name=config.embedding_model)

    vectorstore = init_vectorstore(embeddings_model=embedding_model)

    logger.info("Carregando documentos...")
    docs = load_documents()

    logger.info("Dividindo documentos em chunks...")
    split_docs = split_documents(docs)

    logger.info("Adicionando documentos ao vectorstore...")
    ids = vectorstore.add_documents(documents=split_docs)

    logger.info(f"✓ Vectorstore criado com {len(ids)} chunks")

    return vectorstore


if __name__ == "__main__":
    vectorstore = get_vectorstore()

    # Criar retriever e fazer busca
    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": config.retrieval_k}
    )

    print("\nDigite 'exit' para sair\n")

    while True:
        query = input("Query: ")

        if query.lower() in ["exit", "quit", "sair"]:
            print("Encerrando...")
            break

        if not query.strip():
            continue

        results = retriever.invoke(query)

        print(f"\nResultados para '{query}':")
        for i, doc in enumerate(results, 1):
            print(f"\n--- Resultado {i} ---")
            print(f"Source: {doc.metadata.get('source', 'unknown')}")
            print(f"Content: {doc.page_content}...")
            print(f"\n--- Resultado {i} ---\n")
