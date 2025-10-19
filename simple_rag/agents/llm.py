"""
Agente baseado em Ollama e LangGraph.
"""
import operator
from typing import Literal, List
from typing_extensions import TypedDict, Annotated

from langchain_ollama import ChatOllama
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage, AIMessage
from langgraph.graph import StateGraph, START, END

from simple_rag.tools import add, multiply, retriever
from simple_rag.config import config
from simple_rag.logger import setup_logger

logger = setup_logger(__name__)

# Configuração do LLM
llm = ChatOllama(
    model=config.OLLAMA_MODEL,
    temperature=config.OLLAMA_TEMPERATURE,
    base_url=config.OLLAMA_BASE_URL
)

# Ferramentas disponíveis
tools = [add, multiply, retriever]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

class MessagesState(TypedDict):
    """Estado das mensagens do agente."""
    messages: Annotated[List[AnyMessage], operator.add]
    llm_calls: int

def ollama_call(state: dict):
    """
    LLM decide se deve chamar uma ferramenta ou não.

    Args:
        state: Estado atual com mensagens

    Returns:
        Novo estado com resposta do LLM
    """
    return {
        "messages": [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content="Você é um assistente médico especializado em anamnese. "
                                "Você responde perguntas com base nos documentos disponíveis "
                                "e fornece informações claras e precisas."
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

def tool_node(state: dict):
    """
    Executa as ferramentas chamadas pelo LLM.

    Args:
        state: Estado atual com tool calls

    Returns:
        Novo estado com resultados das ferramentas
    """
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        logger.debug(f"Executando ferramenta: {tool_call['name']}")
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))
    return {"messages": result}

def should_continue(state: MessagesState) -> Literal['tool_node', END]:
    """
    Decide se deve continuar o loop ou parar.

    Args:
        state: Estado atual

    Returns:
        Próximo nó ou END
    """
    messages = state["messages"]
    last_message = messages[-1]

    # Se a LLM faz uma chamada para a tool, então executa a ação
    if last_message.tool_calls:
        return "tool_node"

    # Se não, para e responde ao usuário
    return END

def create_agent():
    """
    Cria e compila o agente médico.

    Returns:
        Agente compilado
    """
    logger.info("Criando agente médico...")

    agent_builder = StateGraph(MessagesState)

    agent_builder.add_node("ollama_call", ollama_call)
    agent_builder.add_node("tool_node", tool_node)
    agent_builder.add_edge(START, "ollama_call")
    agent_builder.add_conditional_edges(
        "ollama_call",
        should_continue,
        ["tool_node", END]
    )
    agent_builder.add_edge("tool_node", "ollama_call")

    logger.info("✓ Agente criado com sucesso")

    return agent_builder.compile()

if __name__ == "__main__":
    agent = create_agent()

    messages = [HumanMessage(content="Add 3 and 4.")]
    logger.info("Testando agente com: Add 3 and 4.")

    result = agent.invoke({"messages": messages})

    for msg in result["messages"]:
        if isinstance(msg, AIMessage):
            msg.pretty_print()
