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

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model
)


def process_query(query:str):
    print("searching chunk", query)
    search_result = vector_db.similarity_search(query=query)

    # Create context
    context = "\n\n".join([
    f"Page content: {result.page_content}\n"
    f"Page Number: {result.metadata.get('page', 'Unknown')}\n"
    f"File Location: {result.metadata.get('source', 'Unknown')}"
    for result in search_result])

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
            "content":query
        }
    ]
)
    print(f"🤖: {response.choices[0].message.content}")
    return response.choices[0].message.content  