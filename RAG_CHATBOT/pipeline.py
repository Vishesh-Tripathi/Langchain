from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory

from Prompts.main import rag_prompt
from embedding import retriever
from LLM.brain import llm



# Conversation history


history = InMemoryChatMessageHistory()



# Format retrieved documents into context


def format_docs(docs):
    return "\n\n".join(
        f"""
Course ID: {doc.metadata.get('course_id')}
Course Name: {doc.metadata.get('course_name')}
Experience Level: {doc.metadata.get('experience_level')}
Duration: {doc.metadata.get('duration')}

{doc.page_content}
"""
        for doc in docs
    )



# Create the RAG chain once


rag_chain = (
    rag_prompt
    | llm
    | StrOutputParser()
)


# Ask the RAG system


def ask_rag(question: str) -> str:

    # 1. Retrieve relevant documents
    docs = retriever.invoke(question)

    # 2. Convert documents into a context string
    context = format_docs(docs)

    # 3. Invoke the RAG chain
    response = rag_chain.invoke({
        "context": context,
        "question": question,
        "history": history.messages
    })

    # 4. Store the conversation
    history.add_user_message(question)
    history.add_ai_message(response)

    # 5. Return the final answer
    return response



# Test (run when executed directly)

if __name__ == "__main__":
    query = input("Enter your question: ")

    while query.lower() not in ["exit", "quit"]:
        answer = ask_rag(query)
        print("\nAnswer:", answer)
        query = input("\nEnter your question (or type 'exit' to quit): ")