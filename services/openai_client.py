# services/openai_client.py
import os
from openai import OpenAI
from services.pinecone_client import query_pinecone

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_answer_with_context(question: str, user: str):
    # 1) Create embedding with the v1 client
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    ).data[0].embedding

    # 2) Retrieve context from Pinecone
    matches = query_pinecone(emb) or []
    context = " ".join([(m["metadata"]["text"] if isinstance(m, dict) else m.metadata.get("text", "")) for m in matches])

    # 3) Chat completion (v1 style)
    prompt = f"User context: {context}\n\nQuestion: {question}\nAnswer:"
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4o" if you prefer
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return {"answer": resp.choices[0].message.content}
