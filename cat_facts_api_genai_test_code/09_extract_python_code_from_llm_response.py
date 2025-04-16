# This is working code with catfact api and splitting json docs
# pip install langchain openai faiss-cpu tiktoken
#pip install langchain-text-splitters
import os
import re
import traceback
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


def extract_between_backticks(text):
    """
    Extracts all the strings between backticks (```) from the given text.
    
    Args:
        text (str): The input text.
    
    Returns:
        list: A list of extracted strings between backticks.
    """
    results = []
    start = 0
    while True:
        start = text.find('```', start)
        if start == -1:
            break
        end = text.find('```', start + 3)
        if end == -1:
            break
        results.append(text[start + 3:end])
        start = end + 3
    return results

os.environ["OPENAI_API_KEY"] = "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"
url = "https://catfact.ninja/docs/api-docs.json"
response = urllib.request.urlopen(url)
data_json = json.loads(response.read())
# print(data_json)

splitter = RecursiveJsonSplitter(max_chunk_size=300)
docs = splitter.create_documents(texts=[data_json])

template = """You are expert automation QA. 

Follow below instructions to generate all possible test cases in Python3 code format for {endpoint}
    1. Use the API schema defined in {context}
    2. Use BaseURL for API as {baseurl}
    3. All API responses are returned in json under "data" key
    4. Use pytest as testing framework
    5. Use positive testing, negative testing, combinatorial testing strategies
    6. Add function to call tests
    7. Dont generate any instructions, generate only code
"""

#model = ChatOpenAI(temperature=0)
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

llm_response = chain.invoke({"context": docs, "baseurl": baseurl, "endpoint": endpoint_spec})
print(llm_response)

if ("```" in llm_response):
    code_snippets = extract_between_backticks(llm_response)
    test_counter = 0
    for code in code_snippets:
        test_counter = test_counter + 1
        print("Code Snippet:")
        code = code.replace("python", "")
        file_name = "generated_test_" + str(test_counter) + ".py"
        print(str(code))
        with open(file_name, 'w') as file:
            file.write(str(code))
else:
    file_name = "generated_test_1.py"
    with open(file_name, 'w') as file:
        file.write(str(llm_response))