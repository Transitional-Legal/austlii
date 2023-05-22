
from llama_index import SimpleDirectoryReader, download_loader, GPTVectorStoreIndex, LLMPredictor, ServiceContext, StorageContext, load_index_from_storage
from llama_index.readers.database import DatabaseReader
from langchain import OpenAI
# from dotenv import find_dotenv, load_dotenv

from data.document import Document

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

import gradio as gr
import os

# load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"] = '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'

# engine = db.create_engine('sqlite:///ftc.db')
# Base = db.declarative_base()

engine = db.create_engine('postgresql://doadmin:AVNS_IWGrvoLyWBBT_TaUS9-@db-postgresql-syd1-64992-do-user-13928987-0.b.db.ondigitalocean.com:25060/tl')
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

# notes https://gpt-index.readthedocs.io/en/latest/guides/primer/usage_pattern.html#optional-save-the-index-for-future-use
def construct_index(directory_path):
    num_outputs = 512

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    print("Loading documents...")
    docs = SimpleDirectoryReader(directory_path).load_data()

    ## Show all files and print them
    for doc in docs:
        save_doc_to_db(doc)


    print("Constructing index...")
    # docs = SimpleDirectoryReader('/home/lucascullen/GitHub/').load_data()

    index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)
    save_index_to_db(index)

    return index


def save_doc_to_db(doc):
    document = Document(filename=doc.doc_id, doc_hash=doc.doc_hash, text=doc.text)
    session.add(document)
    session.commit()


# def construct_google_index(folderid):
#     num_outputs = 512

#     llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))
#     service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

#     print("Loading google documents...")
#     GoogleDriveReader = download_loader("GoogleDriveReader")

#     loader = GoogleDriveReader()

#     print("Constructing index...")
#     docs = loader.load_data(folder_id=folderid)

#     index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)
#     save_index_to_disk(index)

#     return index


def load_index_from_disk():
    storage_context = StorageContext.from_defaults('storage')
    index = load_index_from_storage(storage_context)
    return index


def save_index_to_disk(index):
    index.storage_context.persist()


def save_index_to_db(index):
    # https://gpt-index.readthedocs.io/en/latest/examples/data_connectors/DatabaseReaderDemo.html
    db = DatabaseReader(
        scheme = "postgresql", # Database Scheme
        host = "db-postgresql-syd1-64992-do-user-13928987-0.b.db.ondigitalocean.com", # Database Host
        port = "25060", # Database Port
        user = "doadmin", # Database User
        password = "AVNS_IWGrvoLyWBBT_TaUS9-", # Database Password
        dbname = "tl", # Database Name
    )

    ## db.load_data(index)


def chatbot(input_text):
    # todo: load index from storage
    # just use the index that was already constructed

    # # rebuild storage context
    # storage_context = StorageContext.from_defaults('storage') # storage_context = StorageContext.from_defaults(persist_dir="<persist_dir>")

    # # reload load index
    # index = load_index_from_storage(storage_context)
    
    ## index = GPTVectorStoreIndex.from_documents()
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    return response.response


iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")


# if (os.path.exists("storage") == False):
#     print("Constructing index...")
#     index = construct_index("docs")


# save_doc_to_db()

print("Starting...")

index = construct_index("docs")
# https://drive.google.com/drive/folders/1uNF5mUa-uiPyKUGtUxgBP0Ji9o1eEGv0?usp=sharing
# index = construct_google_index('1uNF5mUa-uiPyKUGtUxgBP0Ji9o1eEGv0')

iface.launch(share=True)
