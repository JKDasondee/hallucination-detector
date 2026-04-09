import anthropic
from server.config import cfg

_c = anthropic.AsyncAnthropic(api_key=cfg.anthropic_api_key)


async def generate(msg: str) -> str:
    r = await _c.messages.create(
        model=cfg.model,
        max_tokens=cfg.max_tokens,
        messages=[{"role": "user", "content": msg}],
    )
    return r.content[0].text
