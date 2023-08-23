import os
import sys
from langchain.llms import LlamaCpp
from transformers import LlamaForCausalLM, LlamaTokenizer
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext

sys.path.insert(0, "/Users/oliverwidder/dev/github/llm/venv/lib/python3.11/site-packages")

llm = LlamaCpp(model_path="/Users/oliverwidder/dev/github/llama.cpp/models/13B/ggml-model-q4_0.bin", verbose=True)
llm_predictor = LLMPredictor(llm=llm)

prompt_helper = PromptHelper()

documents = SimpleDirectoryReader("./docs").load_data()

service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

query_engine = index.as_query_engine()
response = query_engine.query("What is this Python code about?")
print(response)
