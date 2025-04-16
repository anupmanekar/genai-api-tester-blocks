import os
from tools import http_requests_tools
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.llms.openai import OpenAI
from langchain.llms.ollama import Ollama
from langchain_community.agent_toolkits import openapi
from langchain.agents import AgentExecutor, AgentType, initialize_agent

import urllib.request
import json

os.environ["OPENAI_API_KEY"] = ""

url = "https://catfact.ninja/docs/api-docs.json"
response = urllib.request.urlopen(url)
data_json = json.loads(response.read())
# print(data_json)

# model = OpenAI(model="gpt-3.5-turbo", temperature=0)

template = """You are an expert Automation Engineer tasked with analyzing and testing of APIs defined in schema json: {schema}
Using schema please answer the question: {question}
"""

model = Ollama(model="codellama")
prompt = PromptTemplate.from_template(template=template)
tools = [http_requests_tools.invoke_get]
agent = initialize_agent(tools=tools, llm=model, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
prompt.format(schema=data_json, question="What is summary of /breeds endpoint as defined in schema json?")
agent.invoke(prompt)