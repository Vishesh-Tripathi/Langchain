from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-3.5-flash', temperature=0.7, max_output_tokens=1000)
summary_prompt=ChatPromptTemplate.from_template(
   '''You are {topic} expert. Summarize it in 150 words.'''
)
quiz_prompt = ChatPromptTemplate.from_template(''' Based only on the following explanation, create five multiple-choice questions.
Each question must have four options and provide the correct answer.

Explanation:
{explanation} ''' )

summary_chain=summary_prompt | model
quiz_chain=quiz_prompt | model

explaination = summary_chain.invoke({"topic":"Python programming language"}).text
quiz = quiz_chain.invoke({"explanation":explaination}).text

print("Explanation:\n",explaination)
print("\nQuiz:\n",quiz)