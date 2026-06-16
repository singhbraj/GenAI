from typing_extensions import TypedDict 
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    messages: Annotated[list, add_messages]




def chatbot(state:State):
    print("\n\nInside chatbot node", state)
    return {"messages":["Hi, This is a message from Chatbot Node"]}

def samplenode(state:State):
    print("\n\nInside samplenode node",state)
    return {"messages":["Sample Message Appended"]}


graph_builder = StateGraph(State)

# create node & add node
graph_builder.add_node('chatbot', chatbot)
graph_builder.add_node('samplenode', samplenode)

# create edge and add 
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)
# START -> chatbot -> samplenode -> END


# compile the graph 

graph = graph_builder.compile()
updated_state = graph.invoke(State({"messages":["Hi, My name Braj"]}))
print("\n\nupdated_state", updated_state)




