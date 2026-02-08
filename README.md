# JARVIS Assistant

JARVIS is a modular Python assistant that combines voice input, gesture recognition, GUI feedback, and basic automation commands.

## Why this repository is structured this way

The project is organized around **clear module boundaries** and now includes centralized configuration/logging so future features (new command domains, improved models, additional UI layers) can be added with low friction.

- `jarvis_core.py` orchestrates module lifecycle and runtime loops.
- `config.py` centralizes environment-driven runtime settings.
- `logging_config.py` provides structured logging setup.
- `jarvis_main.py` provides an alternate, security-gated interaction flow.
- `jarvis_commands.py` handles intent-style utility commands.
- `modules/` contains reusable domain components (voice, GUI, LLM, gestures, etc.).
- `docs/` stores architecture and contributor-focused project documentation.

---

## Features

- Voice input and text-to-speech output
- Gesture-triggered actions (camera-based)
- Interactive GUI with state feedback
- Device command routing
- Threat-level simulation and alerting
- LLM provider abstraction with fallback handling

---

## Repository layout

```text
.
├── docs/
│   └── ARCHITECTURE.md
├── modules/
│   ├── __init__.py
│   ├── device_controller.py
│   ├── enhanced_gui.py
│   ├── gesture_recognition.py
│   ├── gui_handler.py
│   ├── llm_selector.py
│   ├── personality.py
│   ├── threat_analyzer.py
│   └── voice_interface.py
├── jarvis_commands.py
├── jarvis_core.py
├── jarvis_main.py
├── JARVIS_MANUAL.md
├── requirements.txt
└── README.md
```

---

## Quick start

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Configure environment variables

Create a `.env` file in the repository root:

```env
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

### 3) Run the assistant

Primary orchestrator:

```bash
python jarvis_core.py
```

Alternative workflow with security keyword flow:

```bash
python jarvis_main.py
```

---

## Development standards

- Keep modules focused on one responsibility.
- Prefer explicit error handling over blanket exceptions.
- Keep environment-dependent values in `.env`.
- Keep docs and code structure in sync whenever adding modules.

---

## Maintenance checklist

When you add or update a feature:

1. Update code in the relevant module.
2. Document behavior in `docs/ARCHITECTURE.md` and/or `JARVIS_MANUAL.md`.
3. Add or update tests/scripts used for validation.
4. Ensure formatting and import hygiene is preserved.

---

## License

This project is licensed under the MIT License (if you intend to distribute it, include a `LICENSE` file in the repository root).


## Validation

```bash
pytest -q
```
