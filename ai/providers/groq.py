

# Setup the blazing fast Groq client
from langchain_groq import ChatGroq
from pydantic import SecretStr

def get_groq_llm(model_name: str = "llama-3.3-70b-versatile", groq_api_key: str = "YOUR_GROQ_API_KEY"):
  """Return the Groq LLM provider class."""
  llm = ChatGroq(
    api_key=SecretStr(groq_api_key),
    model=model_name,
  )
  return llm