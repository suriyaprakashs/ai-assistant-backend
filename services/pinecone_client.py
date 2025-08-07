import os
from pinecone import Pinecone, ServerlessSpec
from utils.embedding import embed_file_text

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX")

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(cloud='gcp', region='us-central1')
    )

index = pc.Index(index_name)

def query_pinecone(vector):
    res = index.query(vector=vector, top_k=3, include_metadata=True)
    return res.matches

async def process_and_embed_file(file, user):
    content = await file.read()
    texts = embed_file_text(content, file.filename)
    for chunk in texts:
        index.upsert([(chunk["id"], chunk["vector"], chunk["metadata"])])
    return {"status": "uploaded and embedded", "chunks": len(texts)}
