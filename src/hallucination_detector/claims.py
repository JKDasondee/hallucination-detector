import re
from functools import lru_cache

import spacy

from hallucination_detector.models import Claim

_nlp = None
_OPINION = re.compile(r"^(i think|i believe|i feel|maybe|perhaps|probably|in my opinion|imo)\b", re.I)
_VERIFIABLE_ENTS = {"PERSON", "ORG", "GPE", "LOC", "DATE", "TIME", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL", "EVENT", "FAC", "PRODUCT", "WORK_OF_ART", "LAW", "NORP", "PERCENT"}
_NUM = re.compile(r"\d")


def _load():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


def extract_claims(text: str) -> list[Claim]:
    nlp = _load()
    doc = nlp(text)
    out = []
    for s in doc.sents:
        t = s.text.strip()
        if len(t.split()) < 5:
            continue
        if t.endswith("?"):
            continue
        if _OPINION.match(t):
            continue
        span = doc[s.start:s.end]
        has_ent = any(e.label_ in _VERIFIABLE_ENTS for e in span.ents)
        has_num = bool(_NUM.search(t))
        if has_ent or has_num:
            out.append(Claim(text=t))
    return out
