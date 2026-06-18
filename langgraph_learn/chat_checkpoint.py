from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-mini")


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


DB_URI = "mongodb://admin:admin@localhost:27017"

config = {
    "configurable": {
        "thread_id": "braj"
    }
}

with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph = graph_builder.compile(checkpointer=checkpointer)

    print("\nAssistant: ", end="", flush=True)
    for msg, metadata in graph.stream(
        {"messages": ["Hey, What am I learning?"]},
        config,
        stream_mode="messages"
    ):
        if msg.content and metadata["langgraph_node"] == "chatbot":
            print(msg.content, end="", flush=True)
    print()
