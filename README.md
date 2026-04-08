# Hallucination Detector

LLM response verification system. Generates responses via Claude, extracts claims, cross-references against evidence sources, scores factual accuracy.

## Stack

- **Backend**: FastAPI + anthropic SDK
- **Detection**: spaCy NER + sentence-transformers + ChromaDB (planned)
- **Model**: claude-sonnet-4-20250514

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env  # fill in ANTHROPIC_API_KEY
uvicorn app.main:app --reload
```

## API

```
POST /chat
{
  "message": "string",
  "conversation_id": "string | null"
}
```

Response includes LLM output, extracted claims with verification labels, and overall factual accuracy score.
