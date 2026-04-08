from pydantic import BaseModel


class ChatReq(BaseModel):
    message: str
    conversation_id: str | None = None


class Claim(BaseModel):
    text: str
    evidence: str
    label: str
    score: float


class ChatRes(BaseModel):
    message: str
    response: str
    claims: list[Claim]
    overall_score: float
    conversation_id: str
