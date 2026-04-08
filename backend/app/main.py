from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import r as chat_router

app = FastAPI(title="Hallucination Detector", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
