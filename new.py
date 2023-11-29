from llama_index import SimpleDirectoryReader, LLMPredictor, ServiceContext
from llama_index.vector_stores import RedisVectorStore
from langchain import OpenAI
from llama_index.storage.index_store import RedisIndexStore
from llama_index import StorageContext, load_index_from_storage
from llama_index import VectorStoreIndex
import os

os.environ["OPENAI_API_KEY"] = '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'


# def add_docs_to_index(doc_path):
#     num_outputs = 512

#     llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))
#     service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
#     documents = SimpleDirectoryReader(doc_path).load_data()

#     # index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)
#     # index.storage_context.persist()

#     return index

# from llama_index import VectorStoreIndex, SimpleDirectoryReader


index = None
storage_prompt = input("Enter a storage type: ")

if storage_prompt == "redis":

    vector_store = RedisVectorStore(
        index_name="pg_essays",
        index_prefix="llama",
        redis_url="redis://localhost:6379",
        # redis_url="redis://192.168.1.20:6379",
        overwrite=True,
    )

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)


if storage_prompt == "disk":
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)


if index is None or storage_prompt == "new":
    documents = SimpleDirectoryReader('docs').load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()


# storage_context = StorageContext.from_defaults(persist_dir="./storage")
# index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()


# Keep prompting for input until user enters "quit"
prompt = ""
while prompt != "quit":
    prompt = input("Enter a prompt: ")

    if prompt == "quit":
        break
    
    response = query_engine.query(prompt)
    print(response)
