const http = require('http');
const fetch = require('node-fetch');
const { v4: uuidv4 } = require('uuid');
const { ChromaClient, OllamaEmbeddingFunction } = require("chromadb");

const client = new ChromaClient({path: "http://chroma:8080"});
const embedder = new OllamaEmbeddingFunction({
    url: "http://ollama-embedding:8080/api/embeddings",
    model: "nomic-embed-text"
})

function splitIntoChunks(text) {
    const paragraphs = text.split('\n\n');
    const chunks = [];
    for (let i = 0; i < paragraphs.length; i += 8) {
        chunks.push(paragraphs.slice(i, i + 8).join('\n\n'));
    }
    return chunks;
}

async function startServer() {

    const collection = await client.getOrCreateCollection({
        name: "my_collection",
        embeddingFunction: embedder
    });

    const response = await fetch('https://gitea-gitea.apps.cluster-z5ls6.z5ls6.sandbox481.opentlc.com/starter/INSTRUCTIONS/raw/branch/master/resources/quantumpulse-3000.md');
    if (!response.ok) throw new Error(`Failed to fetch: ${response.statusText}`);
    const text = await response.text();

    const chunks = splitIntoChunks(text);
    for (const chunk of chunks) {
        console.log("Adding chunk");
        await collection.add({
            documents: [chunk],
            ids: [uuidv4()],
        });
    }

    const server = http.createServer(async (req, res) => {
        if (req.method === 'POST' && req.headers['content-type'] === 'text/plain') {
            let body = '';

            req.on('data', chunk => body += chunk.toString());

            req.on('end', async () => {
                try {
                    const results = await collection.query({
                        queryTexts: [body],
                        nResults: 3,
                    });
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify(results));
                } catch (error) {
                    res.writeHead(500, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: error.message }));
                }
            });
        } else {
            res.writeHead(405, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Only POST method with text/plain content-type is supported' }));
        }
    });

    server.listen(8080, () => console.log('Server running on port 8080'));
}

startServer().catch(err => {
    console.error('Error starting server:', err);
    process.exit(1);
});
