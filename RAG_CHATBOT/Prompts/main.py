from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

rag_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a Course Recommendation Assistant.

Answer the user's question using only the provided context.

Rules:
1. Do not invent information.
2. If the answer is not present in the context, say:
   "I do not have enough information in the provided knowledge base."
3. Keep the answer concise.
4. Mention the relevant course when possible.

Context:
{context}
"""
    ),

    MessagesPlaceholder(
        variable_name="history",
        optional=True
    ),

    (
        "human",
        "{question}"
    )
])