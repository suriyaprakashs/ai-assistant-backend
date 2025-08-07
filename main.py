from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from routes.ask import ask_router
from routes.upload import upload_router

app = FastAPI()

app.include_router(ask_router, prefix="/ask")
app.include_router(upload_router, prefix="/upload")

@app.get("/")
def health_check():
    return {"status": "running"}
