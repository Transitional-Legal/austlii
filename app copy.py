
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, ServiceContext
from langchain import OpenAI
import gradio as gr
import os

os.environ["OPENAI_API_KEY"] = 

# notes https://gpt-index.readthedocs.io/en/latest/guides/primer/usage_pattern.html#optional-save-the-index-for-future-use
def construct_index(directory_path):
    num_outputs = 512

    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    docs = SimpleDirectoryReader(directory_path).load_data()

    index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)
    index.storage_context.persist()

    return index


def chatbot(input_text):
    # index = GPTVectorStoreIndex.load_from_disk('index.json')
    # index = GPTVectorStoreIndex.from_documents()
    response = index.query(input_text, response_mode="compact")
    return response.response


iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")


index = construct_index("docs")
iface.launch(share=True)
