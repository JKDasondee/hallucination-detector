# hallucination-detector

**Claim-level hallucination detection for LLM outputs. Three detection modes: RAG + NLI, self-consistency, and coverage.**

## Overview

Decomposes an LLM response into atomic verifiable claims and scores them with one of three approaches:

1. **RAG + NLI** — retrieves evidence from caller-supplied context, scores with DeBERTa NLI
2. **SelfCheckGPT** — no reference needed, checks consistency across multiple LLM samples
3. **Coverage score** — detects selective truth omission by measuring how much evidence the response covers

## Architecture

```
Input text
  → Claim Extractor   (spaCy en_core_web_sm NER + sentence segmentation)
  ├─ With context:    RAG retrieval (ChromaDB / MiniLM) → DeBERTa NLI entailment
  ├─ With samples:    Cross-sample NLI consistency scoring (SelfCheckGPT)
  └─ With evidence:   Semantic coverage fraction (omission risk)
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

### With reference context (RAG + NLI)

```python
from hallucination_detector import detect

result = detect(
    "The Great Wall of China is visible from space",
    context="The Great Wall of China is not visible from space with the naked eye"
)
print(result.score)      # hallucination probability 0–1
```

### Without reference (SelfCheckGPT)

```python
# Sample the same prompt N times from your LLM, pass the samples
samples = [llm(prompt) for _ in range(5)]
result = detect(primary_response, samples=samples)
```

### Coverage score (detect selective omission)

```python
from hallucination_detector import coverage_score, omission_risk

cov = coverage_score(llm_response, evidence_pool=all_relevant_facts)
risk = omission_risk(llm_response, evidence_pool=all_relevant_facts)
```

### REST API

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

## Research

- **RAG + NLI pipeline:** baseline fact verification, evidence-based entailment scoring
- **SelfCheckGPT mode:** [Manakul et al. 2023](https://arxiv.org/abs/2303.08896) — detect hallucinations by sampling consistency
- **Coverage score:** [Chandra et al. 2026](https://arxiv.org/abs/2602.19141) — addresses sycophantic selective truth omission, complements fabrication detection

## Stack

```
Python 3.10+
spaCy · sentence-transformers · ChromaDB · FAISS
cross-encoder/nli-deberta-v3-base · FastAPI
```

MIT License
