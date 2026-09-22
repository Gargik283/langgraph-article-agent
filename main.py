import operator

from langgraph.graph import StateGraph, START, END
from langchain_mistralai.chat_models import ChatMistralAI
from tavily import TavilyClient
from typing_extensions import Annotated, TypedDict
from langchain.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatMistralAI(
    model="ministral-8b-2512",
    mistral_api_key=os.getenv("MISTRALAI_API_KEY")
)

@tool
def get_information(query: str) -> str:
    """Use this tool for information from the Internet

    Args:
        query (str): The query to search for

    Returns:
        str: The search results
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = client.search(query)
    return str(response)

tools = [get_information]
tools_dict = {tool.name : tool for tool in tools}

model_with_tools = model.bind_tools(tools)


class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


def write_article_node(state: State):
    """Write an article based on the messages in the state

    Args:
        state (State): The state containing the messages

    Returns:
        str: The written article
    """

    messages = state["messages"]

    if messages[-1].type == "tool":
        tool_message = messages[-1]
        messages = messages[:-2]

        messages = messages + [
            HumanMessage(
                content=f"Use the following information from the Internet to write or improve the article:\n\n{tool_message.content}"
            )
        ]

    response = model.invoke(messages)

    return {"messages": [response]}


def review_article_node(state: State):
    """Review the article based on the messages in the state
    Use the tools if necessary to get the information
    Mandatory : If you find that the article needs changes, provide feedback on what changes are needed and call the tools to get more information.
    
    If the article is good, just say "The article is good and does not need any changes."

    Args:
        state (State): The state containing the messages

    Returns:
        str: The review of the article
    """

    messages = []

    for message in state["messages"]:
        if message.type == "tool":
            continue

        if message.type == "ai" and message.tool_calls:
            continue

        messages.append(message)

    response = model_with_tools.invoke(
        [
            SystemMessage(
                content="""You are a helpful assistant that reviews articles and provides feedback.
                You can use tools to get information from the Internet:
                """
            )
        ]
        + messages
        + [
            HumanMessage(content="""
                        Review the article and provide information. If you need more information, use the tools. 
                        If the article is good, just say "The article is good and doesnot need any changes."
                        """)
        ]
    )

    return {"messages": [response]}


def internet_search_node(state: State):
    """Search the internet based on the messages in the state"""

    messages = state["messages"]
    last_message = messages[-1]
    tool_call = last_message.tool_calls[0]

    response = get_information.invoke(
        tool_call["args"]["query"]
    )

    return {
        "messages": [
            ToolMessage(
                content=response,
                tool_call_id=tool_call["id"]
            )
        ]
    }


agent_builder = StateGraph(State)


def decide_internet_search(state: State):
    last_message = state["messages"][-1]
    
    if last_message.tool_calls:
        return "internet_search"
    else:
        return END


agent_builder.add_node("write_article", write_article_node)
agent_builder.add_node("review_article", review_article_node)
agent_builder.add_node("internet_search", internet_search_node)

agent_builder.add_edge(START, "write_article")
agent_builder.add_edge("write_article", "review_article")
agent_builder.add_conditional_edges(
    "review_article",
    decide_internet_search,
    ["internet_search", END]
)
agent_builder.add_edge("internet_search", "write_article")

agent = agent_builder.compile()

response = agent.invoke({
    "messages": [
        HumanMessage(
            content="Write an article about the benefits of meditation."
        )
    ]
})

print(response["messages"][-2].pretty_print())
print(response["messages"][-1].pretty_print())