
from langchain_ollama import ChatOllama

# Connect to the Gemma model running in Ollama
model = ChatOllama(
    model="gemma4:e2b",
    temperature=0, #the lower the temperature, the more deterministic the output
    num_ctx=4096, #context window size, the maximum number of tokens the model can consider at once
)

# Ask the model a question
response = model.invoke(
    "Explain the difference between inflation "
    "and deflation in simple terms."
)

print(response.content)
