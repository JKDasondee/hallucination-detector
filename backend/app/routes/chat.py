import uuid
from fastapi import APIRouter
from app.models import ChatReq, ChatRes
from app.services.llm import generate
from app.services.detector import detect

r = APIRouter()


@r.post("/chat", response_model=ChatRes)
async def chat(req: ChatReq):
    cid = req.conversation_id or str(uuid.uuid4())
    resp = await generate(req.message)
    claims, score = await detect(resp)
    return ChatRes(
        message=req.message,
        response=resp,
        claims=claims,
        overall_score=score,
        conversation_id=cid,
    )
