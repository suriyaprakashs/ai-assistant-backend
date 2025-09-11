# utils/embedding.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_file_text(file_bytes, filename):
    text = file_bytes.decode("utf-8", errors="ignore")
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    embedded = []
    for i, chunk in enumerate(chunks):
        vector = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        ).data[0].embedding
        embedded.append({
            "id": f"{filename}-{i}",
            "vector": vector,
            "metadata": {"text": chunk}
        })
    return embedded
