# JARVIS Architecture

## 1. Runtime entry point

### `jarvis_core.py`
The primary orchestrator now follows a cleaner runtime lifecycle:
- loads typed runtime settings from `config.py`,
- configures structured logging from `logging_config.py`,
- initializes domain modules,
- dispatches commands through a prefix-to-handler routing table,
- runs voice, threat-monitoring, and gesture loops concurrently.

## 2. Configuration and observability

### `config.py`
- Defines a typed `JarvisConfig` dataclass.
- Centralizes env-driven settings (API keys + loop intervals).

### `logging_config.py`
- Provides one-time logging bootstrap used by the runtime.

## 3. Module boundaries (`modules/`)

- `voice_interface.py`: speech recognition + TTS abstraction.
- `gesture_recognition.py`: camera and gesture detection loop.
- `enhanced_gui.py`: interactive visual shell and status display.
- `gui_handler.py`: lightweight GUI utility variant.
- `llm_selector.py`: model provider routing with fallback strategy.
- `device_controller.py`: typed registration and action dispatch.
- `personality.py`: conversational tone shaping.
- `threat_analyzer.py`: threat scoring and alert messages.

## 4. Command routing contract

`jarvis_core.py` supports prefixed command domains:
- `llm:<query>`
- `device:<device action>`
- `gesture:<gesture_name>`
- `threat:<context>`
- `personality:<message>`

Unknown commands receive a safe fallback response.

## 5. Testing strategy

`tests/` now includes focused unit coverage for:
- device registration and command dispatch,
- runtime command routing behavior,
- core command utility behavior.

These tests validate core business logic without requiring full GUI, camera, or microphone execution.
