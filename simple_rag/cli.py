"""Interface de linha de comando para o Simple RAG."""

from langchain_core.messages import AIMessage, HumanMessage

from simple_rag.agents.llm import create_agent
from simple_rag.config import config
from simple_rag.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Ponto de entrada principal."""
    logger.info("=" * 60)
    logger.info("Simple RAG - Assistente")
    logger.info(f"Modelo: {config.ollama_model}")
    logger.info(f"Ollama URL: {config.ollama_base_url}")
    logger.info("=" * 60)

    try:
        agent = create_agent()
    except Exception as e:
        logger.error(f"Erro ao criar agente: {e}")
        logger.error("Verifique se o Ollama esta rodando e o modelo esta disponovel")
        print("\nL Erro ao inicializar o agente.")
        print("   Verifique se o Ollama esta rodando: ollama serve")
        print(
            f"   Verifique se o modelo esta disponivel: ollama pull {config.ollama_model}"
        )
        return

    print("\n" + "=" * 60)
    print("Simple RAG - Assistente")
    print("=" * 60)
    print("Digite suas perguntas. Para sair, digite 'exit'\n")

    while True:
        try:
            user_input = input("Voce: ")

            if user_input.lower() in ["exit", "quit", "sair"]:
                logger.info("Encerrando...")
                print("\nAte logo!")
                break

            if not user_input.strip():
                continue

            messages = [HumanMessage(content=user_input)]

            logger.debug(f"Processando: {user_input}")
            result = agent.invoke({"messages": messages})

            for msg in result["messages"]:
                if isinstance(msg, AIMessage):
                    print(f"\nAssistente: {msg.content}\n")

        except KeyboardInterrupt:
            logger.info("\nInterrompido pelo usu�rio")
            print("\n\nAte logo!")
            break
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)
            print(f"\nL Erro: {e}\n")


if __name__ == "__main__":
    main()
