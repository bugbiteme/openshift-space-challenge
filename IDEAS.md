# Game Ideas

## RAG to the rescue

You've replaced the ship's broken engine, but the AI that operates it
doesn't know how it works.  Fortunately we have an operating manual.
We'll implement a RAG system so the AI can learn about the operation
of the engine.

We'll need to generate a lengthy engine manual in markdown format.
This should be easy for chatgpt or similar.  We can host the text file
in gitea for players and player should be able to curl it directly
(using .raw url).

We would have to host one model somewhere to generate embeddings.

The series of challenges would look something like this:

### Deploy a chromadb vector database on OpenShift.
The flag can be some text chromadb prints at startup

### Split the manual up by markdown section
The flag is the number of sections

### Create an embedding for the first section
The flag is the first number in the embedding vector

### Populate the vectordb with all of the embeddings
Not sure about flag here

### Implement a web service that will be called by the AI
The AI will call a web service you need to implement.
We can provide a curl command that players can test with.
The API will be a post of some text.
You need to create an embedding for that text, and
look it up in the vectordb and return the text.
Asking the AI to try this should be triggered manually by the player somehow.
The AI presents the flag once it knows it can look up things like "How do I
start the engine?"  "What kind of fuel does the engine take?"
