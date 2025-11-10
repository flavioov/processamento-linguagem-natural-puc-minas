"""Agente baseado em Ollama e LangGraph."""

import operator
from typing import Annotated, Literal, TypedDict

from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

from simple_rag.config.config import settings
from simple_rag.tools import add, multiply, retrieve_context
from simple_rag.utils.logger import setup_logger

logger = setup_logger(__name__)

# Configuração do LLM
llm = ChatOllama(
    model=settings.ollama_model,
    temperature=settings.ollama_temperature,
    base_url=settings.ollama_base_url,
)

# Ferramentas disponíveis
tools = [add, multiply, retrieve_context]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)


class MessagesState(TypedDict):
    """Estado das mensagens do agente."""

    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


def ollama_call(state: MessagesState):
    """LLM decide se deve chamar uma ferramenta ou não.

    Args:
        state: Estado atual com mensagens

    Returns:
        Novo estado com resposta do LLM
    """
    messages: list[AnyMessage] = [
        SystemMessage(content=settings.system_message),
        *state["messages"],
    ]
    return {
        "messages": [llm_with_tools.invoke(messages)],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


def tool_node(state: MessagesState):
    """Executa as ferramentas chamadas pelo LLM.

    Args:
        state: Estado atual com tool calls

    Returns:
        Novo estado com resultados das ferramentas
    """
    result = []
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            tool = tools_by_name[tool_call["name"]]
            logger.debug(f"Executando ferramenta: {tool_call['name']}")
            observation = tool.invoke(tool_call["args"])
            result.append(
                ToolMessage(content=str(observation), tool_call_id=tool_call["id"])
            )
    return {"messages": result}


def should_continue(state: MessagesState) -> Literal["tool_node", "__end__"]:
    """Decide se deve continuar o loop ou parar.

    Args:
        state: Estado atual

    Returns:
        Próximo nó ou END
    """
    messages = state["messages"]
    last_message = messages[-1]

    # Se a LLM faz uma chamada para a tool, então executa a ação
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tool_node"

    # Se não, para e responde ao usuário
    return "__end__"


def create_agent():
    """Cria e compila o agente médico.

    Returns:
        Agente compilado
    """
    logger.info("Criando agente médico...")

    agent_builder = StateGraph(MessagesState)

    agent_builder.add_node("ollama_call", ollama_call)
    agent_builder.add_node("tool_node", tool_node)
    agent_builder.add_edge(START, "ollama_call")
    agent_builder.add_conditional_edges(
        "ollama_call", should_continue, ["tool_node", END]
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
