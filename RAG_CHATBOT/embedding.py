from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from dotenv import load_dotenv

from splitter import chunks

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    output_dimensionality=768,
)

vectorstore = InMemoryVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

print("Vector store created.")