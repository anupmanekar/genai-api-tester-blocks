from langchain_community.llms import Ollama

llm = Ollama(model="codellama")

code = llm.invoke("Generate python testing code for REST API 'https://catfact.ninja/breed'")

print(code)