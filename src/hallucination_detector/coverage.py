from typing import Any

import numpy as np

_encoder: Any = None


def _get_encoder() -> Any:
    global _encoder
    if _encoder is None:
        from sentence_transformers import SentenceTransformer

        _encoder = SentenceTransformer("all-MiniLM-L6-v2")
    return _encoder


def coverage_score(response: str, evidence_pool: list[str]) -> float:
    if not evidence_pool or not response.strip():
        return 0.0
    m = _get_encoder()
    resp_emb = m.encode(response, convert_to_numpy=True)
    ev_emb = m.encode(evidence_pool, convert_to_numpy=True)
    norms = np.linalg.norm(resp_emb) * np.linalg.norm(ev_emb, axis=1)
    norms = np.where(norms == 0, 1e-10, norms)
    sims = (resp_emb @ ev_emb.T) / norms
    covered = int(np.sum(sims > 0.4))
    return round(covered / len(evidence_pool), 4)


def omission_risk(response: str, evidence_pool: list[str]) -> float:
    return round(1.0 - coverage_score(response, evidence_pool), 4)
