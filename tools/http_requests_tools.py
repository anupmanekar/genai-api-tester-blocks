import requests
from json import JSONDecoder
from langchain.tools import tool


@tool("HTTP GET Client", return_direct=True)
def invoke_get(url: str) -> requests.Response: 
    """Invoke HTTP GET calls for given url"""
    response = requests.get(url)
    return response
