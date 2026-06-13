from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(str(pdf_path))

docs = loader.load()

print(docs[2])

# Split the docs into smaller chunk


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_text(documents = docs)