import anthropic
from app.config import cfg

_c = anthropic.Anthropic(api_key=cfg.anthropic_api_key)


async def generate(msg: str) -> str:
    r = _c.messages.create(
        model=cfg.model,
        max_tokens=cfg.max_tokens,
        messages=[{"role": "user", "content": msg}],
    )
    return r.content[0].text
