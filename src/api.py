from flask import Flask
from llama_index import SimpleDirectoryReader
from llama_index.vector_stores import RedisVectorStore
from llama_index import StorageContext, load_index_from_storage

from llama_index import VectorStoreIndex
# from llama_index import VectorStoreIndex, SimpleDirectoryReader
from dotenv import load_dotenv
import requests
import os

load_dotenv()
app = Flask(__name__)

os.environ["OPENAI_API_KEY"] = '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'
query_engine = None


def load(matter):
    vector_store = RedisVectorStore(
        index_name=matter, index_prefix="llama", redis_url=os.getenv('REDIS_URL'), overwrite=False)

    # Load the index from storage
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query_engine = index.as_query_engine()


def add_docs_to_redis(doc_path, matter):

    url = 'https://au.app.clio.com/api/v4/documents.json'

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    url = f'https://au.app.clio.com/api/v4/documents/{id}/download.json'
    response = requests.request("GET", url, headers=headers)

    with open("gdp_by_country.zip", mode="wb") as file:
        file.write(response.content)

    # print(response.text)

    # https://gpt-index.readthedocs.io/en/latest/examples/vector_stores/RedisIndexDemo.html
    documents = SimpleDirectoryReader(doc_path).load_data()

    vector_store = RedisVectorStore(
        index_name=matter,
        index_prefix="llama",
        redis_url=os.getenv('REDIS_URL'),
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


# Do this on webhook
@app.route('/documents/', methods=['POST'])
def load_matter(matter):

    # get matter id from request body
    # matter = request.json['matter']

    add_docs_to_redis(matter)
    load(matter)
    return "Loaded"


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
