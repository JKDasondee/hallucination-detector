import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from hallucination_detector import detect

r = APIRouter()


class DetectReq(BaseModel):
    text: str
    context: str | None = None


class ClaimOut(BaseModel):
    text: str
    evidence: str
    label: str
    score: float


class DetectRes(BaseModel):
    text: str
    claims: list[ClaimOut]
    score: float
    request_id: str


class ChatReq(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatRes(BaseModel):
    message: str
    response: str
    claims: list[ClaimOut]
    overall_score: float
    conversation_id: str


@r.post("/detect", response_model=DetectRes)
async def detect_endpoint(req: DetectReq) -> DetectRes:
    result = detect(req.text, context=req.context)
    return DetectRes(
        text=result.text,
        claims=[ClaimOut(text=c.text, evidence=c.evidence, label=c.label.value, score=c.score) for c in result.claims],
        score=result.score,
        request_id=str(uuid.uuid4()),
    )


@r.post("/chat", response_model=ChatRes)
async def chat(req: ChatReq) -> ChatRes:
    cid = req.conversation_id or str(uuid.uuid4())
    try:
        from server.llm import generate

        resp = await generate(req.message)
    except Exception:
        resp = req.message
    result = detect(resp)
    return ChatRes(
        message=req.message,
        response=resp,
        claims=[ClaimOut(text=c.text, evidence=c.evidence, label=c.label.value, score=c.score) for c in result.claims],
        overall_score=result.score,
        conversation_id=cid,
    )
