from enum import Enum

from pydantic import BaseModel, Field


class Label(str, Enum):
    VERIFIED = "verified"
    HALLUCINATED = "hallucinated"
    UNCERTAIN = "uncertain"


class Claim(BaseModel):
    text: str
    evidence: str = ""
    label: Label = Label.UNCERTAIN
    score: float = Field(default=0.5, ge=0.0, le=1.0)


class DetectionResult(BaseModel):
    text: str
    claims: list[Claim]
    score: float = Field(default=0.5, ge=0.0, le=1.0)
