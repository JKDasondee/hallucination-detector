import numpy as np
from sentence_transformers import CrossEncoder

from hallucination_detector.models import Claim, Label

_model: CrossEncoder | None = None


def _get_model() -> CrossEncoder:
    global _model
    if _model is None:
        _model = CrossEncoder("cross-encoder/nli-deberta-v3-base")
    return _model


def score_claims(claims: list[Claim]) -> list[Claim]:
    m = _get_model()
    out = []
    for c in claims:
        if not c.evidence:
            out.append(c.model_copy(update={"score": 0.5, "label": Label.UNCERTAIN}))
            continue
        logits = np.asarray(m.predict([(c.text, c.evidence)]))
        probs = _softmax(logits[0])
        cont, _, ent = probs[0], probs[1], probs[2]
        if ent > 0.7:
            lb = Label.VERIFIED
        elif cont > 0.5:
            lb = Label.HALLUCINATED
        else:
            lb = Label.UNCERTAIN
        out.append(c.model_copy(update={"score": round(float(cont), 4), "label": lb}))
    return out


def _softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x))
    result: np.ndarray = e / e.sum()
    return result
