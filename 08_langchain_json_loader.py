#pip install langchain-text-splitters
#pip install --upgrade --quiet  lark chromadb
import os
import requests
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = ""

json_data = requests.get("https://catfact.ninja/docs/api-docs.json").json()

splitter = RecursiveJsonSplitter(max_chunk_size=300)

json_chunks = splitter.split_json(json_data=json_data)

docs = splitter.create_documents(texts=[json_data])
print("--------------------------------------------------")
print(docs[2])
print("--------------------------------------------------")

vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
""" retriever = vectorstore.as_retriever()

response = retriever.get_relevant_documents("what are the parameters for /breeds endpoint?")

print(response) """

document_content_description = "Schema json for CatFacts API"
llm = ChatOpenAI(temperature=0)
retriever = SelfQueryRetriever.from_llm(
    llm,
    vectorstore,
    document_content_description,
    None)

retriever.invoke("What are the parameters for /breeds endpoint?")

