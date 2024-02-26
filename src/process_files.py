from llama_index.vector_stores import RedisVectorStore
from llama_index import SimpleDirectoryReader
from langchain import OpenAI
from llama_index.storage.storage_context import StorageContext
from llama_index import VectorStoreIndex
from dotenv import load_dotenv
import requests
import os

load_dotenv()

# Vector store
count = 0
os.environ["OPENAI_API_KEY"] = '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'

def add_docs_to_redis(doc_path, matter):
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + os.environ["CLIO_API_KEY"]
    }

    url = 'https://au.app.clio.com/api/v4/documents.json'
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)

    id = 59543995
    url = f'https://au.app.clio.com/api/v4/documents/{id}.json?fields=id,name'
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)

    response_dict = response.json()
    name = response_dict['data']['name']


    url = f'https://au.app.clio.com/api/v4/documents/{id}/download.json'
    response = requests.request("GET", url, headers=headers)
    # print(response.text)

    with open(f"temp/{name}", mode="wb") as file:
        file.write(response.content)


    # https://gpt-index.readthedocs.io/en/latest/examples/vector_stores/RedisIndexDemo.html
    documents = SimpleDirectoryReader(doc_path).load_data()

    count = documents.__len__()

    vector_store = RedisVectorStore(
        index_name=matter,
        index_prefix="llama",
        redis_url="redis://localhost:6379",
        overwrite=False,
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context)

    os.remove(f"temp/{name}")

    return index


def add_docs_to_local_disk(doc_path):
    documents = SimpleDirectoryReader(doc_path).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()

    return index


add_docs_to_redis('temp', '252028')
print("Done adding docs to redis")
