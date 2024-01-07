from flask import Flask
from llama_index import SimpleDirectoryReader #, LLMPredictor, ServiceContext
from llama_index.vector_stores import RedisVectorStore
# # from langchain import OpenAI
# # from llama_index.storage.index_store import RedisIndexStore
from llama_index import StorageContext, load_index_from_storage

from llama_index import VectorStoreIndex
# from llama_index import VectorStoreIndex, SimpleDirectoryReader
import os

app = Flask(__name__)

os.environ["OPENAI_API_KEY"] = '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'
query_engine = None


def load():
    vector_store = RedisVectorStore(
        index_name="pg_essays",
        index_prefix="llama",
        redis_url="redis://localhost:6379",
        # redis_url="rediss://default:AVNS_UeoUo9p18wxjLj6DyMT@db-redis-syd1-25631-do-user-7279278-0.b.db.ondigitalocean.com:25061",
        overwrite=True,
    )

    # Load the index from storage
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query_engine = index.as_query_engine()


def add_docs_to_redis(doc_path):
    # https://gpt-index.readthedocs.io/en/latest/examples/vector_stores/RedisIndexDemo.html
    documents = SimpleDirectoryReader(doc_path).load_data()

    # count = documents.__len__()

    vector_store = RedisVectorStore(
        index_name="pg_essays",
        index_prefix="llama",
        redis_url="redis://localhost:6379",
        # redis_url="rediss://default:AVNS_UeoUo9p18wxjLj6DyMT@db-redis-syd1-25631-do-user-7279278-0.b.db.ondigitalocean.com:25061",
        overwrite=True,
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context)

    return index


@app.route('/query/<prompt>', methods=['GET'])
def query(prompt):
    if query_engine is None:
        load()
    response = query_engine.query(prompt)
    return response


@app.route('/load/', methods=['POST'])
def welcome():
    # time the load time
    add_docs_to_redis('cases')
    load()
    return "Loaded"
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

    