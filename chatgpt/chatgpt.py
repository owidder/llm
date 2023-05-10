from llama_index import SimpleDirectoryReader, GPTListIndex, LLMPredictor, ServiceContext
from langchain import OpenAI
import os
from datetime import datetime

os.environ["OPENAI_API_KEY"] = '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'


def construct_index(directory_path):
    num_outputs = 512
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    docs = SimpleDirectoryReader(directory_path).load_data()
    index = GPTListIndex.from_documents(docs, service_context=service_context)

    return index


index = construct_index("docs")
query_engine = index.as_query_engine()
print(datetime.now())
response = query_engine.query("What is a knotterbex policy? Please answer in not more than 3 sentences!")
print(response)
print(datetime.now())
response = query_engine.query("Are knotterbex policies efficient? Please answer in not more than 3 sentences!")
print(response)
print(datetime.now())
