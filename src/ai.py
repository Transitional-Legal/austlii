from db import Db
from llama_index import SimpleDirectoryReader, download_loader, GPTVectorStoreIndex, LLMPredictor, ServiceContext, StorageContext, load_index_from_storage
from llama_index import OpenAI


class Ai:

    def __init__(self):
        self.num_outputs = 512
        # self.index = self.load_index()

    def chatbot(self, input_text):
        # todo: load index from storage
        # just use the index that was already constructed

        # # rebuild storage context
        # storage_context = StorageContext.from_defaults('storage') # storage_context = StorageContext.from_defaults(persist_dir="<persist_dir>")

        # # reload load index
        # index = load_index_from_storage(storage_context)

        # index = GPTVectorStoreIndex.from_documents()
        query_engine = self.index.as_query_engine()
        response = query_engine.query(input_text)
        return response.response

    def load_index(self):
        llm_predictor = LLMPredictor(llm=OpenAI(
            temperature=0.7, model_name="text-davinci-003", max_tokens=self.num_outputs))
        docs = Db.load_docs()
        
        self.service_context = ServiceContext.from_defaults(
            llm_predictor=llm_predictor)
        self.index = GPTVectorStoreIndex.from_documents(docs)
        
        return index
