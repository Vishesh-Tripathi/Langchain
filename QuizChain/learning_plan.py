from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="empero-ai/Qwythos-9B-Claude-Mythos-5-1M",
    temperature=0.7
)
model = ChatHuggingFace(llm=llm)
prompt = ChatPromptTemplate.from_messages([

    ('system',"You are a schedule planner who can create a learning plan for a given topic based on the user's experience."),
    ('human','I want to learn {topic} and my experience is {experience}. Can you create a learning plan for me?')
])

chain = prompt | model
result = chain.invoke({
    "topic": "Python programming language",
    "experience": "I have basic knowledge of programming and I am familiar with concepts like variables, loops, and functions."
})
print(result.text)