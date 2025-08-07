import openai, os
from services.pinecone_client import query_pinecone

openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_answer_with_context(question, user):
    embedding = openai.Embedding.create(input=question, model="text-embedding-3-small")["data"][0]["embedding"]
    matches = query_pinecone(embedding)
    context = " ".join([m["metadata"]["text"] for m in matches])
    prompt = f"User context: {context}\n\nQuestion: {question}\nAnswer:"
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"answer": response.choices[0].message.content}
