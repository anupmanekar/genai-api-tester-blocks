# pip install langchain openai faiss-cpu tiktoken
#pip install langchain-text-splitters
import os
import re
import traceback
from sys import argv
from operator import itemgetter

from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.llms.ollama import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import urllib.request
import json
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveJsonSplitter

#os.environ["OPENAI_API_KEY"] = ""

# petstore.json contains limited paths and not full json
with open('petstore.json') as f:
    data_json = json.load(f)

print(data_json)
url = "https://petstore.swagger.io/v2/swagger.json"
response = urllib.request.urlopen(url)
# data_json = json.loads(response.read())

system_instructions = """You are expert automation QA code generator who uses below instructions to generate possible tests in Python3 code format:

    1. Use the API schema defined in {context}
    2. Note body parameters, path parameters, query parameters and header parameters for {path}
    3. Use BaseURL for API as {baseurl}
    4. All API responses are returned in json under "data" key
    5. Use positive testing, negative testing, combinatorial testing strategies
    6. Use only pytest as testing framework
    7. Do not generate any recommendations/instructions on usage of pytest or python
"""

human_instructions = """
Write a code to test endpoint {path} for method {method}
"""

splitter = RecursiveJsonSplitter(max_chunk_size=300)
docs = splitter.create_documents(texts=[data_json])

code_gen_prompt = ChatPromptTemplate.from_template(template=human_instructions)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_instructions),
        ("human", human_instructions),
    ]
)
model = ChatOllama(model="codellama")
chain = final_prompt | model
#x = chain.invoke({"context": data_json,"baseurl":"https://petstore.swagger.io/v2/",  "endpoints": "/pet/{petId}", "method": "delete"})
#print(str(x.content))


#prompt = ChatPromptTemplate.from_template(template=human_instructions)
#chain = create_stuff_documents_chain(model, prompt)
llm_response = chain.invoke({"context": data_json,"baseurl":"https://petstore.swagger.io/v2/",  "path": "/pet", "method": "post"})
print(llm_response.content)