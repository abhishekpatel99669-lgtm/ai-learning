from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

# LLM
llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)


# State
class State(TypedDict):
    message: Annotated[list, add_messages]


# Chatbot node
def chatbot(state: State):
    response = llm.invoke(state["message"])

    return {
        "message": [response]
    }


# Build graph
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


# MongoDB
DB_URL = "mongodb://abhi:abhi@localhost:27017"

with MongoDBSaver.from_conn_string(DB_URL) as checkpointer:

    graph_with_checkpointer = graph_builder.compile(
        checkpointer=checkpointer
    )

    config = {
        "configurable": {
            "thread_id": "1"#user_id
        }
    }

    for chunk in graph_with_checkpointer.stream(
        {
            "message": [
                {
                    "role": "user",
                    "content": "Hi, My name is Abhishek Patel"
                }
            ]
        },
        config
    ):

       for chunk in graph_with_checkpointer.stream(
            {
                "message": [
                    {
                        "role": "user",
                        "content": "What am I learning?"
                   }
                ]
            },
            config,
            stream_mode="values"
        ):
           chunk["message"][-1].pretty_print()
        

# from dotenv import load_dotenv
# # from fastapi.datastructures import State
# from typing_extensions import TypedDict
# from typing import Annotated
# from langgraph.graph.message import add_messages
# from langgraph.graph import StateGraph, START, END
# from langchain.chat_models import init_chat_model
# from langgraph.checkpoint.mongodb import MongoDBSaver

# load_dotenv()

# llm=init_chat_model(
#     model="gpt-4.1-mini",
#     model_provider="openai"
# )

# class State(TypedDict):
#     message: Annotated[list,add_messages]

# def chatbot(state: State):
#     response=llm.invoke(state["message"])
#     return{"message": [response]}



# graph_builder = StateGraph(State)
# graph_builder.add_node(chatbot, "chatbot")

# graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("chatbot", END)

# graph = graph_builder.compile()

# def compile_graph_with_checkpointer(checkpointer):
#     return graph_builder.compile(checkpointer=checkpointer)
# DB_URL = "mongodb://abhi:abhi@localhost:27017"
# with MongoDBSaver.from_conn_string(DB_URL) as checkpointer:
#     graph = graph_builder.compile(checkpointer=checkpointer)
    

#     # graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer)

#     config = {
#         "configurable": {
#             "thread id": "1"

#             }
#         }
         
#     updated_state = graph_with_checkpointer.invoke(
#     State({"message": ["Hi, My name is Abhishek Patel"]}),
#     config,
#     )

# print("\n\nupdated_state", updated_state)

#     updated_state= graph_with_checkpointer.invoke(
#         State({"message": ["Hi, My name is Abhishek Patel"]}),
#         config,
#         )
# print("\n\nupdated_state", updated_state)

#START -> chatbot ->   END
#State = {message: {Hey there!}}
#Node Runs: chatbot(State[Hey there!]) -> {message: ["Hi, I'am a chatbot how can help you?"]}

# checkpointer(Abhishek) = Hi my name is Abhishek Patel