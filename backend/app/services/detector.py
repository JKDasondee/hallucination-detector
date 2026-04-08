from app.models import Claim


async def detect(text: str) -> tuple[list[Claim], float]:
    return [], 1.0
