# JARVIS Architecture

## 1. Runtime entry points

### `jarvis_core.py`
Primary orchestrator that:
- initializes all modules,
- starts GUI,
- runs background loops for voice, gestures, and threat monitoring,
- routes user commands to domain modules.

### `jarvis_main.py`
Alternate flow with:
- wake-word + security activation model,
- command queue processing,
- conversational wrappers around `jarvis_commands.execute_command`.

## 2. Module boundaries (`modules/`)

- `voice_interface.py`: speech recognition + TTS abstraction.
- `gesture_recognition.py`: camera and gesture detection logic.
- `enhanced_gui.py`: advanced visual interface and interaction elements.
- `gui_handler.py`: lighter GUI handling utility.
- `llm_selector.py`: provider routing (OpenAI/Hugging Face/local fallback).
- `device_controller.py`: device registration and action dispatch.
- `personality.py`: tone/response behavior.
- `threat_analyzer.py`: threat level analysis and alert message generation.

## 3. Command routing

- `jarvis_core.py` interprets prefixed command domains (`llm:`, `device:`, `gesture:`, `threat:`, `personality:`).
- `jarvis_main.py` forwards natural-language commands to `jarvis_commands.py`.
- `jarvis_commands.py` handles utility intents (time, date, web, weather, system info, conversation).

## 4. Configuration

Environment variables are loaded from `.env` where applicable:
- `OPENAI_API_KEY`
- `HUGGINGFACE_API_KEY`
- `OPENWEATHER_API_KEY`

## 5. Improvement roadmap

1. Introduce tests for command routing and module contracts.
2. Unify `jarvis_core.py` and `jarvis_main.py` under a single configurable runtime mode.
3. Add structured logging (levels + log sinks) instead of print-based diagnostics.
4. Add typed configuration object to replace scattered env lookups.
