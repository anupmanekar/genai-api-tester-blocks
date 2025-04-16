# pip install langchain openai faiss-cpu tiktoken
#pip install langchain-text-splitters
import os
import re
import traceback
from sys import argv
from operator import itemgetter

from langchain.prompts import ChatPromptTemplate
from langchain.llms.ollama import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import urllib.request
import json
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_text_splitters import RecursiveJsonSplitter

os.environ["OPENAI_API_KEY"] = ""
url = "https://petstore.swagger.io/v2/swagger.json"
response = urllib.request.urlopen(url)
data_json = json.loads(response.read())

humman_qa_template = """Generate all possible test cases in Python3 code format for {endpoints}.

Use below instructions while generating the tests:
    1. Use BaseURL for API as {baseurl}
    2. Use Basic Authentication parameters as username - anup and password - admin123
    3. Use positive testing, negative testing, combinatorial testing strategies
    4. All tests should be part of single code snippet
    5. Dont generate any instructions, generate only code
"""

system_qa_template = """You are expert automation QA experienced in testing REST API. Use following instructions while generating any tests.

    1. Use OPEN API specification in JSON format as context: {context}
    2. Consider path parameters, query parameters and header parameters in "parameters" key while generating tests based on parameters
    3. Consider 200, 400 and 404 responses in "responses" key while generating tests based on responses
    4. All API responses are returned in json under "data" key
    5. Use pytest as testing framework
    6. Use requests as http request library
"""

system_template = """You are expert automation QA experienced in testing REST API. Use following instructions to answering any questions:

    1. Use OPEN API specification in JSON format as context: {context}. 
    2. Consider only "parameters" key while answering questions on parameters.
    3. Consider only "responses" key while answering questions on responses.
    4. If you cannot answer question, say "I dont know"
"""

parameters_question_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("human", "What are the query, path and header parameters in {method} of {endpoint} ?"),
    ]
)

responses_question_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("human", "What are different responses expected in {method} of {endpoint} ?"),
    ]
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_qa_template),
        ("human", humman_qa_template),
    ]
)

model = ChatOllama(model="codellama", temperature=0.0)
chain = parameters_question_prompt | model
qa_chain = qa_prompt | model
#x = chain.invoke({"context": data_json, "endpoint": "/pet/{petId}", "method": "delete"})
x = qa_chain.invoke({"context": data_json,"baseurl":"https://petstore.swagger.io/v2/",  "endpoints": "/pet/{petId}", "method": "delete"})
print(str(x.content))