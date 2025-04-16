import os
from langchain import hub
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOllama
from langchain.chains import RetrievalQA


MY_LANGCHAIN_HUB_KEY = ""

os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com" # Update with your API URL if using a hosted instance of Langsmith.
os.environ["LANGCHAIN_API_KEY"] = MY_LANGCHAIN_HUB_KEY # Update with your API key
os.environ["LANGCHAIN_HUB_API_URL"] = "https://api.hub.langchain.com" # Update with your API URL if using a hosted instance of Langsmith.
os.environ["LANGCHAIN_HUB_API_KEY"] = MY_LANGCHAIN_HUB_KEY # Update with your Hub API key

# Loads the latest version
print("Data loading")
prompt = hub.pull("rlm/rag-prompt", api_url="https://api.hub.langchain.com")
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
data = loader.load()

print("Data splitting")
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
all_splits = text_splitter.split_documents(data)

print("Store splits")
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OllamaEmbeddings())

print("Initialize LLM")
llm = ChatOllama(model_name="codellama", temperature=0)

print("Initializing Chain")
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": prompt}
)

question = "What are the approaches to Task Decomposition?"
result = qa_chain({"query": question})
print(result["result"])