from dotenv import load_dotenv
import os

load_dotenv()

print("✅ PINECONE_API_KEY =", os.getenv("PINECONE_API_KEY"))
print("✅ PINECONE_INDEX =", os.getenv("PINECONE_INDEX"))
print("✅ OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("✅ SUPABASE_JWT_SECRET =", os.getenv("SUPABASE_JWT_SECRET"))
