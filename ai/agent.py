from ai.providers.groq import get_groq_llm
from ai.providers.ollama import get_ollama_llm


def get_llm_provider(apiKey:str, llm_name: str, model_name: str):
  """As per user preference, return the LLM provider class."""
  print(f"Api Key: {apiKey}, LLM Provider: {llm_name}, Model: {model_name}")
  if llm_name.lower() == "groq":
    return get_groq_llm(model_name=model_name,groq_api_key=apiKey)
  if llm_name.lower() == "ollama":
    return get_ollama_llm(model_name=model_name)
  raise ValueError(f"Unsupported LLM provider: {llm_name}")



