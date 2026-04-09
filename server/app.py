import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes import r as api_router

app = FastAPI(title="Hallucination Detector", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


def cli() -> None:
    try:
        import uvicorn
    except ImportError:
        print("Install server extras: pip install hallucination-detector[server]")
        sys.exit(1)

    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["serve"])
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--host", default="0.0.0.0")
    a = p.parse_args()
    if a.command == "serve":
        uvicorn.run("server.app:app", host=a.host, port=a.port, reload=True)
