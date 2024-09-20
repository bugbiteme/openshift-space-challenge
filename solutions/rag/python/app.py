import base64
import chromadb
import uuid, requests, time
from ollama_embedding_function import OllamaEmbeddingFunction
from flask import Flask, request, jsonify

app = Flask(__name__)

client = chromadb.HttpClient(host="chroma", port=8080)
 
def split_into_chunks(text):
    paragraphs = text.split('\n\n')
    return [ '\n\n'.join(paragraphs[i:i + 8])
            for i in range(0, len(paragraphs), 8)]

def setup():
    global collection
    collection = client.create_collection("my_collection", 
                                         embedding_function=OllamaEmbeddingFunction(url="http://ollama-embedding:8080/api/embeddings", model_name="nomic-embed-text"),
                                          get_or_create=True)
    url = 'https://gitea-gitea.apps.cluster-hx2ll.hx2ll.sandbox834.opentlc.com/starter/INSTRUCTIONS/raw/branch/master/resources/quantumpulse-3000.md'
    response = requests.get(url)
    text = response.text
    chunks = split_into_chunks(text)
    if False:   # We only need to do this once.
        for chunk in chunks:
            print ("embedding")
            print(collection.add(documents=[chunk], ids=[str(uuid.uuid4())]))

@app.route('/', methods=['POST'])
def hello():
    if request.content_type == 'text/plain':
        body = request.data.decode('utf-8')
        try:
            results = collection.query(query_texts=[body], n_results=3)
            print(results)
            return jsonify(results), 200
        except Exception as e:
            return jsonify({'error', str(e)}), 500
    else:
        return jsonify({'error': 'Bad'}), 405

setup()
app.run(host="0.0.0.0", port=8080)

