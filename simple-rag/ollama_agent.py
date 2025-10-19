import operator

from typing import Literal, List
from typing_extensions import TypedDict, Annotated
from IPython.display import Image, display

from langchain_ollama import ChatOllama
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, START, END

from ollama_tools import add, multiply, retriever

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
    base_url="http://11.7.0.2:11434"
)

tools = [add, multiply, retriever]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

class MessagesState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    llm_calls: int

def ollama_call(state: dict):
    """LLM decides whether to call a tool or not"""
    return {
        "messages": [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content="Você é um residente em clinica geral e sempre responde a pergunta, mas adiciona sarcasmo e cansaço."
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


def should_continue(state: MessagesState) -> Literal['tool_node', END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # se a llm faz uma chamada para a 'tool', então faz uma ação
    if last_message.tool_calls:
        return "tool_node"

    # se não, para e responde ao usuário
    return END


def agent():
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

    return agent_builder.compile()


if __name__ == "__main__":

    agent = agent()
    # display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

    messages = [HumanMessage(content="Add 3 and 4.")]
    print("invoking agent .... ")
    messages = agent.invoke({"messages": messages})
    for m in messages["messages"]:
        m.pretty_print()
