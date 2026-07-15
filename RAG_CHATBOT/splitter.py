from langchain_text_splitters import RecursiveCharacterTextSplitter
from document_processor import documents

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)
chunks = splitter.split_documents(documents)

# print(f"Number of chunks: {len(chunks)}")
# for i, chunk in enumerate(chunks, start=1):
#     print(f"\n--- Chunk {i} ---")
#     print(chunk.page_content.strip())
