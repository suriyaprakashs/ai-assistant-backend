from fastapi import APIRouter, File, UploadFile, Depends
from services.pinecone_client import process_and_embed_file
from services.supabase_auth import verify_token

upload_router = APIRouter()

@upload_router.post("/")
async def upload_file(file: UploadFile = File(...), user=Depends(verify_token)):
    return await process_and_embed_file(file, user)
