from pathlib import Path
from flask import Flask, request
# from langchain import OpenAI
# from llama_index import GPTVectorStoreIndex, LLMPredictor, ServiceContext, download_loader
# from ai import Ai
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world'


@app.route('/index', methods=['POST'])
def index():
    if request.method == 'POST':

        f = request.files['file']
        f.save(secure_filename(f.filename))
        print (secure_filename(f.filename))

        # num_outputs = 512

        # llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))
        # # docs = SimpleDirectoryReader(directory_path).load_data()

        # ImageReader = download_loader("ImageReader")
        # imageLoader = ImageReader(text_type="plain_text")
        # FlatPdfReader = download_loader("FlatPdfReader")
        # pdfLoader = FlatPdfReader(image_loader=imageLoader)

        # doc = pdfLoader.load_data(file=Path(secure_filename(f.filename)))

        # service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
        # index = GPTVectorStoreIndex.from_documents(doc, service_context=service_context)
        # return index
        return secure_filename(f.filename)
