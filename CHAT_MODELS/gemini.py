from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-3.5-flash",temperature=0.7, max_output_tokens=256)
result = model.invoke("Write a poem about the moon.")
print(result.text)