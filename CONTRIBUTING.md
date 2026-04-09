# Contributing

1. Fork and clone
2. `pip install -e ".[dev]"`
3. `python -m spacy download en_core_web_sm`
4. Make changes
5. `ruff check src/ tests/ && pytest`
6. Open a PR

Code style: ruff. No comments. Type hints required.
