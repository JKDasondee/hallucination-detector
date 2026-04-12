from typing import Any

import numpy as np

from hallucination_detector.models import Claim, Label

_model: Any = None


def _get_nli_model() -> Any:
    global _model
    if _model is None:
        from sentence_transformers import CrossEncoder

        _model = CrossEncoder("cross-encoder/nli-deberta-v3-base")
    return _model


def _softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x))
    result: np.ndarray = e / e.sum()
    return result


def selfcheck_nli(claim: str, samples: list[str]) -> float:
    if not samples:
        return 0.5
    m = _get_nli_model()
    pairs = [(s, claim) for s in samples]
    logits = np.asarray(m.predict(pairs))
    scores = []
    for row in logits:
        probs = _softmax(row)
        scores.append(float(probs[0]))
    return float(np.mean(scores))


def score_by_consistency(claims: list[Claim], samples: list[str]) -> list[Claim]:
    if not samples:
        return claims
    out = []
    for c in claims:
        contradiction = selfcheck_nli(c.text, samples)
        if contradiction > 0.5:
            lb = Label.HALLUCINATED
        elif contradiction < 0.2:
            lb = Label.VERIFIED
        else:
            lb = Label.UNCERTAIN
        out.append(c.model_copy(update={"score": round(contradiction, 4), "label": lb}))
    return out
