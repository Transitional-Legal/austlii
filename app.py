
from llama_index import SimpleDirectoryReader, GithubRepositoryReader, GPTVectorStoreIndex, LLMPredictor, ServiceContext
from langchain import OpenAI
from dotenv import find_dotenv, load_dotenv

import gradio as gr
import os

load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"] = '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'

# notes https://gpt-index.readthedocs.io/en/latest/guides/primer/usage_pattern.html#optional-save-the-index-for-future-use
def construct_index(directory_path):
    num_outputs = 512

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    docs = SimpleDirectoryReader(directory_path).load_data()
    # docs = SimpleDirectoryReader('/home/lucascullen/GitHub/').load_data()

    index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)
    index.storage_context.persist()

    return index


def construct_gh_index():
    num_outputs = 512

    github_token = os.environ.get("GITHUB_TOKEN")
    owner = "horse-link"
    repo = "contracts.horse.link"
    branch = "main"

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    docs = GithubRepositoryReader(
        github_token=github_token,
        owner=owner,
        repo=repo,
        use_parser=False,
        verbose=False,
    ).load_data(branch=branch)

    index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)
    index.storage_context.persist()

    return index


def chatbot(input_text):
    ## index = GPTVectorStoreIndex.load_from_disk('index.json')
    index = GPTVectorStoreIndex.from_documents()
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    return response.response


iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")


index = construct_index("docs")
iface.launch(share=True)
