

# Setup the blazing fast Groq client
from langchain_groq import ChatGroq
from pydantic import SecretStr

def get_groq_llm(model_name: str = "llama-3.3-70b-versatile", groq_api_key: str = "YOUR_GROQ_API_KEY"):
  """Return the Groq LLM provider class."""
  kwargs = {}
  if model_name.startswith("openai/gpt-oss"):
    # gpt-oss models spend part of the output budget on hidden reasoning
    # before the final answer; leaving max_tokens unset let a multi-day
    # structured workout plan get cut off mid-array once that budget ran out.
    # reasoning_effort keeps that hidden budget small so max_tokens (which
    # Groq reserves against the account's TPM cap for the whole request)
    # can stay low enough to fit under the 8000 TPM on-demand limit.
    kwargs["reasoning_effort"] = "low"

  llm = ChatGroq(
    api_key=SecretStr(groq_api_key),
    model=model_name,
    max_tokens=6000,
    **kwargs,
  )
  return llm