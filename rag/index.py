from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(str(pdf_path))

load_dotenv()

docs = loader.load()

print(docs[2])

# Split the docs into smaller chunk


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(documents=docs)

# Vextor Embeddings 

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="rag"
)

print("Indexing of documents done.")