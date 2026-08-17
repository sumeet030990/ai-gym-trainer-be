

# Setup the blazing fast Groq client
from langchain_ollama import ChatOllama

def get_ollama_llm(model_name: str = "gemma4"):
  """Return the Ollama LLM provider class."""
  llm = ChatOllama(
    model=model_name,
    num_ctx=8192,
    temperature=0.3,
  )
  return llm