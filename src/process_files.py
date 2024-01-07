from llama_index.vector_stores import RedisVectorStore
from llama_index import SimpleDirectoryReader
from langchain import OpenAI
from llama_index.storage.storage_context import StorageContext
from llama_index import VectorStoreIndex
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

os.environ["OPENAI_API_KEY"] = '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'

# Vector store
count = 0

def add_docs_to_redis(doc_path):
    # https://gpt-index.readthedocs.io/en/latest/examples/vector_stores/RedisIndexDemo.html
    documents = SimpleDirectoryReader(doc_path).load_data()

    count = documents.__len__()

    vector_store = RedisVectorStore(
        index_name="pg_essays",
        index_prefix="llama",
        redis_url="redis://localhost:6379",
        # redis_url="redis://192.168.1.20:6379",
        overwrite=True,
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context)

    return index


def add_docs_to_local_disk(doc_path):
    documents = SimpleDirectoryReader(doc_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()

    return index


add_docs_to_redis('docs')
print("Done adding docs to redis")
