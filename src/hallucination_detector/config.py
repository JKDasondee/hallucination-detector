from dataclasses import dataclass, field


@dataclass
class Config:
    claim_model: str = "spacy"
    retriever_backend: str = "chromadb"
    scorer_model: str = "cross-encoder/nli-deberta-v3-base"
    device: str = "cpu"
    extra: dict[str, object] = field(default_factory=dict)
