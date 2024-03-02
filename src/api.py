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


temp_path = 'docs'

# Fetch all documents for a matter to the temp_path to be added to the index
def fetch_matter_docs(matter_id):
    url = f'https://au.app.clio.com/api/v4/documents.json?matter_id={matter_id}'
    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_dict = response.json()
    documents = response_dict['documents']

    for doc in documents:
        doc_id = doc['id']
        doc_name = doc['file_name']
        url = f'https://au.app.clio.com/api/v4/documents/{doc_id}/download.json'
        response = requests.request("GET", url, headers=headers)

        with open(f"{temp_path}/{doc_name}", mode="wb") as file:
            file.write(response.content)



def fetch_single_doc(doc_id):
    url = f'https://au.app.clio.com/api/v4/documents/{doc_id}/download.json'
    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_dict = response.json()
    documents = response_dict['documents']

    for doc in documents:
        doc_id = doc['id']
        doc_name = doc['file_name']
        url = f'https://au.app.clio.com/api/v4/documents/{doc_id}/download.json'
        response = requests.request("GET", url, headers=headers)

        with open(f"{temp_path}/{doc_name}", mode="wb") as file:
            file.write(response.content)


def load(matter):
    vector_store = RedisVectorStore(
        index_name=matter, index_prefix="llama", redis_url=os.getenv('REDIS_URL'), overwrite=False)

    # Load the index from storage
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query_engine = index.as_query_engine()


def add_docs_to_redis(doc_path, matter, delete=True):
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


    # if delete:
    #     os.remove(doc_path)

    return index


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/query/<prompt>', methods=['GET'])
def query(prompt):
    if query_engine is None:
        load()
    response = query_engine.query(prompt)
    return response


@app.route('/index/<matter>', methods=['POST'])
def index_matter():
    fetch_matter_docs(matter)
    add_docs_to_redis('matter')
    load()
    return "Loaded"


# When a new document is created on Clio, it should be added to the index
@app.route('/documents/', methods=['POST'])
def add_document(matter):

    # get matter id from request body
    # matter = request.json['matter']

    add_docs_to_redis(matter)
    load(matter)
    return "Loaded"


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080)
