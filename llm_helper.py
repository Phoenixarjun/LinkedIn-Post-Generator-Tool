from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os



load_dotenv()

llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"),model_name="llama-3.3-70b-versatile")


if __name__ == "__main__":
    response = llm.invoke("What is the capital of France?")
    print(response)
    # Example output: "The capital of France is Paris."