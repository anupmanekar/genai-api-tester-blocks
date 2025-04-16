from langchain.agents import create_json_agent
from langchain_community.agent_toolkits import JsonToolkit
from langchain_community.tools.json.tool import JsonSpec
from langchain.llms.ollama import Ollama
from langchain_openai import OpenAI
import urllib.request
import json
import os

os.environ["OPENAI_API_KEY"] = ""

url = "https://catfact.ninja/docs/api-docs.json"
response = urllib.request.urlopen(url)
data_json = json.loads(response.read())
print(data_json)

json_spec = JsonSpec(dict_=data_json, max_value_length=4000)
json_toolkit = JsonToolkit(spec=json_spec)

json_agent_executor = create_json_agent(
    llm=OpenAI(temperature=0), toolkit=json_toolkit, verbose=True
)

json_agent_executor.run(
    "What are the parameters in /breeds endpoint?"
)