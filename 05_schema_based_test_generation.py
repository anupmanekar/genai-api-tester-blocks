# pip install langchain openai faiss-cpu tiktoken
#pip install langchain-text-splitters
import os
from sys import argv
from operator import itemgetter

from langchain.prompts import ChatPromptTemplate
from langchain.llms.ollama import Ollama
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import urllib.request
import json
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveJsonSplitter

os.environ["OPENAI_API_KEY"] = ""
url = "https://catfact.ninja/docs/api-docs.json"
response = urllib.request.urlopen(url)
data_json = json.loads(response.read())
# print(data_json)

splitter = RecursiveJsonSplitter(max_chunk_size=300)
docs = splitter.create_documents(texts=[data_json])

template = """You are expert automation QA. Please follow below instructions to generate all possible test cases in Python3 code format for {endpoints}
    1. Use the API schema defined in {context}
    2. Use BaseURL for API as {baseurl}
    3. Use Basic Authentication parameters as username - anup and password - admin123
    4. Use positive testing, negative testing, combinatorial testing strategies
"""

# model = ChatOpenAI(temperature=0)
model = Ollama(model="codellama")
prompt = ChatPromptTemplate.from_template(template=template)
chain = create_stuff_documents_chain(model, prompt)
# test_generation_chain = (
#     {"context": data_json} 
#     | prompt 
#     | model 
#     | StrOutputParser()
# )

# x = test_generation_chain.invoke(input=argv[1])
# print(x)
baseurl = "https://catfact.ninja"
endpoint_spec = "/facts"

x = chain.invoke({"context": docs, "baseurl": baseurl, "endpoints": endpoint_spec})
print(x)