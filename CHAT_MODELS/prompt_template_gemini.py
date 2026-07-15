from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0.7,
    max_output_tokens=500
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful health information assistant."),
    ("human", "I am having this {problem} with my health. Can you help me?")
])

chain = prompt | model

result = chain.invoke({
    "problem": "headache"
})

print(result.text)