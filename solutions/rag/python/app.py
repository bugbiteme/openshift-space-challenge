from flask import Flask, request, jsonify
import requests
import uuid
from chromadb import ChromaClient, OllamaEmbeddingFunction

app = Flask(__name__)

client = ChromaClient(path='http://chroma:8080')
embedder = OllamaEmbeddingFunction(
    url='http://ollama-embedding:8080/api/embeddings',
    model='nomic-embed-text'
)

def split_into_chunks(text, paragraphs_per_chunk=8):
    paragraphs = text.split('\n\n')
    return [ '\n\n'.join(paragraphs[i:i + paragraphs_per_chunk])
             for i in range(0, len(paragraphs), paragraphs_per_chunk) ]

@app.before_first_request
def setup():
    global collection
    collection = client.get_or_create_collection(name='my_collection', embedding_function=embedder)

    url = 'https://gitea-gitea.apps.cluster-z5ls6.z5ls6.sandbox481.opentlc.com/starter/INSTRUCTIONS/raw/branch/master/resources/quantumpulse-3000.md'
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful

    text = response.text
    chunks = split_into_chunks(text)

    for chunk in chunks:
        collection.add(documents=[chunk], ids=[str(uuid.uuid4())])

@app.route('/', methods=['POST'])
def handle_request():
    if request.content_type == 'text/plain':
        body = request.data.decode('utf-8')
        try:
            results = collection.query(query_texts=[body], n_results=3)
            return jsonify(results), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Only POST method with text/plain content-type is supported'}), 405

if __name__ == '__main__':
    app.run(port=8080)
