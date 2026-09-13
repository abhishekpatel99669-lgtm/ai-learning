from dotenv import load_dotenv

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()



pdf_path=Path(__file__).parent/"python_PDF.pdf"

#lode this file in python program
loader=PyPDFLoader(file_path=pdf_path)
doc=loader.load()

# print(doc[20])
#split the docs into smaller chunks
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
chunks=text_splitter.split_documents(documents=doc)

#Vector Embeddings
embedding_model=OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_store=QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

print("Indexing of document done...")

