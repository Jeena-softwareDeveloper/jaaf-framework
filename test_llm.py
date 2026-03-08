from langchain_community.chat_models import ChatOllama
from config import settings

def test_llm():
    print(f"Testing ChatOllama with URL: {settings.OLLAMA_URL}")
    llm = ChatOllama(
        model="tinyllama",
        base_url=settings.OLLAMA_URL
    )
    try:
        response = llm.invoke("Say hi")
        print(f"LLM Response: {response.content}")
    except Exception as e:
        print(f"LLM Failed: {e}")

if __name__ == "__main__":
    test_llm()
