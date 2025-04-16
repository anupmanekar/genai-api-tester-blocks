# https://docs.llamaindex.ai/en/stable/examples/query_engine/json_query_engine/

import logging
import sys
import os
import openai

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
os.environ["OPENAI_API_KEY"] = "YOUR_KEY_HERE"
