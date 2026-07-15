from embedding import retriever
question = "I am an SAP ABAP developer with no AI experience. Which course should I take first to learn SAP Business AI?"

retrieved_docs = retriever.invoke(question)

for i, doc in enumerate(retrieved_docs, start=1):
    print(f"--- Retrieved document {i} ---")
    print(doc.page_content.strip())
    print("Source:", doc.metadata.get("source"))
    print()