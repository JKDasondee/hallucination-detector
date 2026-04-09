[![CI](https://github.com/JKDasondee/hallucination-detector/actions/workflows/ci.yml/badge.svg)](https://github.com/JKDasondee/hallucination-detector/actions) [![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

# hallucination-detector

Detect hallucinations in LLM outputs. Claim-level extraction, evidence retrieval, NLI scoring.

## Install

```bash
pip install hallucination-detector
```

## Quick Start

```python
from hallucination_detector import detect

result = detect(
    "The Great Wall of China is visible from space",
    context="The Great Wall of China is not visible from space with the naked eye"
)

print(result.score)        # 0.87 — high hallucination probability
print(result.claims[0])    # Claim(text="Great Wall visible from space", label="hallucinated", ...)
```

Without context (uses built-in knowledge retrieval):

```python
result = detect("Albert Einstein invented the telephone")
```

## How It Works

1. **Claim Extraction** — Break LLM response into atomic verifiable claims (spaCy NER + rules)
2. **Evidence Retrieval** — Find supporting/contradicting evidence (ChromaDB + sentence-transformers)
3. **NLI Scoring** — Score each claim against evidence (cross-encoder entailment model)
4. **Aggregation** — Combine scores into final hallucination probability (sklearn ensemble)

## As an API Server

```bash
pip install hallucination-detector[server]
hallucination-detector serve --port 8000
```

```bash
curl -X POST http://localhost:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Einstein invented the telephone"}'
```

## Pipeline Architecture

```
Input Text -> Claim Extractor -> Evidence Retriever -> NLI Scorer -> Aggregator -> Result
                  |                    |                 |              |
             spaCy NER          ChromaDB/FAISS    cross-encoder    sklearn
             + rules         + sentence-transformers   (NLI)     ensemble
```

## Optional Dependencies

```bash
pip install hallucination-detector[ml]         # spaCy, sentence-transformers, torch, sklearn
pip install hallucination-detector[retrieval]   # ChromaDB, FAISS
pip install hallucination-detector[server]      # FastAPI, uvicorn, anthropic
pip install hallucination-detector[all]         # everything
```

## Development

```bash
git clone https://github.com/jaydasondee/hallucination-detector.git
cd hallucination-detector
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

## Benchmarks

Run with `python benchmarks/evaluate.py` against the labeled `benchmarks/dataset.json` (30 hand-curated claim/context pairs, 16 hallucinated / 14 verified):

| Metric    | Value   |
|-----------|---------|
| Accuracy  | 96.7%   |
| Precision | 100.0%  |
| Recall    | 93.8%   |
| F1 Score  | 96.8%   |
| Latency   | 0.94s / claim |

Larger benchmarks (TruthfulQA, HaluEval, FEVER) are in progress.

## Status

| Component | Status | Model |
|-----------|--------|-------|
| Claim extraction | Working | spaCy `en_core_web_sm` NER + sentence segmentation |
| Evidence retrieval | Working | `all-MiniLM-L6-v2` dense cosine similarity |
| NLI scoring | Working | `cross-encoder/nli-deberta-v3-base` |
| Aggregation | Working | Weighted mean |
| API server | Working | FastAPI |
| PyPI package | Planned | |
| Benchmarks | In progress | TruthfulQA, HaluEval |

## License

MIT
