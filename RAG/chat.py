# from dotenv import load_dotenv
# from openai import OpenAI

# from langchain_openai import OpenAIEmbeddings
# from langchain_qdrant import QdrantVectorStore

# load_dotenv()

# openai_client=OpenAI()


# #Vector Embeddings
# embedding_model=OpenAIEmbeddings(
#     model="text-embedding-3-large"
# )

# vector_db=QdrantVectorStore.from_existing_collection(
#     url="http://localhost:6333",
#     collection_name="learning_rag",
#     embedding=embedding_model
# )

# #Takes the user input
# user_query=("Ask somethinks: ")
# #Relevant chunk from the vector db
# search_result=vector_db.similarity_search(query=user_query)

# context = "\n\n".join([
#     f"Page content: {result.page_content}\n"
#     f"Page Number: result.metadata['page_table']\n"
#     f"File Location: {result.metadata['source']}"
#     for result in search_result
# ])

# SYSTEM_PROMTS=f"""
# You are a helpfull AI assistant you answers user queries based on the avalable content retrieved from the PDF files along with page_context and page_number.

# You should only ans the user based on the following context and nevigate the user to open the right page to know more.

# Context:
# {context}
# """

# response=openai_client.chat.completions.create(
#     model="gpt-4o-mini",
#     message=[
#         {"role":"system", "content":SYSTEM_PROMTS},
#          {"role":"user", "content":user_query}
#     ]
# )

# print(f"🤖:{response.choices[0].message.content}")
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

openai_client = OpenAI()

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Connect to Qdrant
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model
)

# Take user input
user_query = input("Ask something: ")

# Relevant chunks from vector database
search_result = vector_db.similarity_search(
    query=user_query
)

# Create context
context = "\n\n".join([
    f"Page content: {result.page_content}\n"
    f"Page Number: {result.metadata.get('page', 'Unknown')}\n"
    f"File Location: {result.metadata.get('source', 'Unknown')}"
    for result in search_result
])

SYSTEM_PROMPT = f"""
You are a helpful AI assistant.

Answer the user's query only using the context retrieved
from the PDF files.

Mention the relevant page number and file location when possible.

If the answer cannot be found in the provided context,
say that the information is not available in the PDF.

Context:

{context}
"""

response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_query
        }
    ]
)

print(f"🤖: {response.choices[0].message.content}")