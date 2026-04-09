import re

import numpy as np

from hallucination_detector.models import Claim

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _split_sentences(txt: str) -> list[str]:
    parts = re.split(r'(?<=[.!?])\s+', txt.strip())
    return [p for p in parts if len(p) > 5]


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(a) * np.linalg.norm(b, axis=1)
    n = np.where(n == 0, 1e-10, n)
    return (a @ b.T) / n


def retrieve_evidence(claims: list[Claim], context: str | None = None, k: int = 3) -> list[Claim]:
    if not context or not claims:
        return claims

    sents = _split_sentences(context)
    if not sents:
        return claims

    m = _get_model()
    s_emb = m.encode(sents, convert_to_numpy=True)

    for c in claims:
        q = m.encode(c.text, convert_to_numpy=True)
        sims = _cosine_sim(q, s_emb)
        idx = np.argsort(sims)[::-1][:k]
        c.evidence = " ".join(sents[i] for i in idx)

    return claims
