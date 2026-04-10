# hallucination-detector

**Claim-level hallucination detection for LLM outputs. spaCy NER extraction, ChromaDB RAG evidence retrieval, DeBERTa NLI scoring.**

## Overview

Decomposes an LLM response into atomic verifiable claims, retrieves supporting or contradicting evidence, scores each claim via natural language inference, and aggregates into a final hallucination probability. Works with or without caller-supplied context; without context it falls back to built-in vector retrieval.

## Architecture

```
Input text
  → Claim Extractor   (spaCy en_core_web_sm NER + sentence segmentation)
  → Evidence Retriever (ChromaDB / FAISS + all-MiniLM-L6-v2 cosine similarity)
  → NLI Scorer        (cross-encoder/nli-deberta-v3-base entailment scoring)
  → Aggregator        (weighted mean → hallucination probability 0–1)
  → DetectionResult   (per-claim labels + aggregate score)
```

## Install

```bash
pip install hallucination-detector
```

Optional dependency groups:

```bash
pip install hallucination-detector[ml]         # spaCy, sentence-transformers, torch, sklearn
pip install hallucination-detector[retrieval]   # ChromaDB, FAISS
pip install hallucination-detector[server]      # FastAPI, uvicorn
pip install hallucination-detector[all]
```

## Usage

```python
from hallucination_detector import detect

result = detect(
    "The Great Wall of China is visible from space",
    context="The Great Wall of China is not visible from space with the naked eye"
)

print(result.score)      # hallucination probability 0–1
print(result.claims)     # per-claim label + evidence
```

REST API:

```bash
hallucination-detector serve --port 8000

curl -X POST http://localhost:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Einstein invented the telephone"}'
```

## Results

Evaluated on 30 hand-curated claim/context pairs (16 hallucinated, 14 verified):

| Metric    | Value  |
|-----------|--------|
| Accuracy  | 96.7%  |
| Precision | 100.0% |
| Recall    | 93.8%  |
| F1        | 96.8%  |
| Latency   | 0.94s / claim |

Reproduce: `python benchmarks/evaluate.py`

## Stack

```
Python 3.10+
spaCy · sentence-transformers · ChromaDB · FAISS
cross-encoder/nli-deberta-v3-base · FastAPI
```

MIT License
