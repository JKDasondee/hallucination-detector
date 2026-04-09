[![CI](https://github.com/JKDasondee/hallucination-detector/actions/workflows/ci.yml/badge.svg)](https://github.com/JKDasondee/hallucination-detector/actions) [![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

# hallucination-detector

Claim-level hallucination detection for LLM outputs.

The pipeline extracts verifiable claims, retrieves supporting or contradicting evidence, scores each claim with an NLI model, and aggregates the results into a final hallucination score.

## Status

Research prototype. The core pipeline, tests, CI, and FastAPI server are implemented. PyPI publishing and larger public benchmarks are not done yet.

## Install

This package is not published to PyPI yet.

```bash
git clone https://github.com/JKDasondee/hallucination-detector.git
cd hallucination-detector
pip install -e ".[all]"
```

## Quick Start

```python
from hallucination_detector import detect

result = detect(
    "The Great Wall of China is visible from space",
    context="The Great Wall of China is not visible from space with the naked eye"
)

print(result.score)
print(result.claims[0])
```

Without explicit context, the retriever tries to gather supporting evidence before scoring the claims.

## How It Works

1. Claim extraction with spaCy + rules
2. Evidence retrieval with dense similarity search
3. Claim scoring with a cross-encoder NLI model
4. Aggregation into a final hallucination probability

## Run As An API Server

```bash
hallucination-detector serve --port 8000
```

```bash
curl -X POST http://localhost:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Einstein invented the telephone"}'
```

## Pipeline

```text
Input text
  -> claim extraction
  -> evidence retrieval
  -> NLI scoring
  -> aggregation
  -> final detection result
```

## Optional Dependencies

```bash
pip install -e ".[ml]"
pip install -e ".[retrieval]"
pip install -e ".[server]"
pip install -e ".[all]"
```

## Development

```bash
pytest
ruff check src tests
mypy src
```

## Benchmark

Run with `python benchmarks/evaluate.py` against `benchmarks/dataset.json`.

Current sanity-set results on 30 hand-curated claim/context pairs:

| Metric    | Value |
|-----------|-------|
| Accuracy  | 96.7% |
| Precision | 100.0% |
| Recall    | 93.8% |
| F1 Score  | 96.8% |
| Latency   | 0.94s / claim |

This is a smoke-test benchmark, not a definitive public leaderboard result. Larger evaluations on TruthfulQA, HaluEval, and FEVER are still pending.

## Components

| Component | Status | Notes |
|-----------|--------|-------|
| Claim extraction | Working | spaCy + sentence segmentation + rules |
| Evidence retrieval | Working | dense retrieval |
| NLI scoring | Working | cross-encoder entailment model |
| Aggregation | Working | weighted score aggregation |
| API server | Working | FastAPI |
| PyPI release | Planned | not published yet |
| Large benchmarks | In progress | TruthfulQA, HaluEval, FEVER |

## License

MIT