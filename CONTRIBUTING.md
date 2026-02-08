# Contributing Guide

## Development setup

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure `.env` for optional API-backed features.

## Coding expectations

- Keep classes and functions single-purpose.
- Use descriptive docstrings for externally called methods.
- Avoid broad exception handling unless there is a documented fallback path.
- Update docs when behavior changes.

## Validation

At minimum, run:

```bash
python -m compileall .
```

Optionally run project-specific scripts/tests as they are added.
