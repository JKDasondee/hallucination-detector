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

Coming soon — evaluation against RAGAS, Vectara HHEM, SelfCheckGPT on standard datasets.

## Status

Active development. Core pipeline shipping week of Apr 14.

| Component | Status |
|-----------|--------|
| Claim extraction | In progress |
| Evidence retrieval | Planned |
| NLI scoring | Planned |
| Aggregation | Planned |
| API server | Working |
| PyPI package | Planned |

## License

MIT
