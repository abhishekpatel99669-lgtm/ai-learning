from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional, Literal
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()

client = OpenAI()

class State(TypedDict):
    user_query: str
    llm : Optional[str]
    is_good:Optional[bool]

def chatbot(state: State):
    print("chatbot node:", state)
    response = client.chat.completions.create(
        model = "gpt-4.1-mini",
        messages = [
            {"role": "user", "content":state["user_query"]}
        ]
    )

    state["llm"]= response.choices[0].message.content
    return state

def evaluate_node(state: State) -> Literal["chatbot_gemini", "endnode"]:
    print("evaluate_node node:", state)
    if True:
        return "endnode"
    
    return"chatbot_gemini"

def chatbot_gemini(state: State):
    print("chatbot_gemini node:", state)
    response = client.chat.completions.create(
        model = "gpt-4.1-mini",
        messages = [
            {"role": "user", "content":state["user_query"]}
        ]
    )

    state["llm"]= response.choices[0].message.content
    return state

def endnode(state:State):
    print("endnode node:", state)
    return state

graph_builder=StateGraph(State)

graph_builder.add_node(chatbot, "chatbot")
graph_builder.add_node(chatbot_gemini, "chatbot_gemini")
graph_builder.add_node(endnode, "endnode")

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", evaluate_node)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)

graph=graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "Hi, What is the largest river in india?"}))

print("\n\nupdated_state", updated_state)