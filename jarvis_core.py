"""Primary JARVIS runtime orchestrator."""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable

from config import JarvisConfig
from logging_config import configure_logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.device_controller import DeviceController
    from modules.enhanced_gui import EnhancedGUI
    from modules.gesture_recognition import GestureRecognition
    from modules.llm_selector import LLMSelector
    from modules.personality import PersonalityModule
    from modules.threat_analyzer import ThreatAnalyzer
    from modules.voice_interface import VoiceInterface

configure_logging()
logger = logging.getLogger(__name__)


class JarvisCore:
    """Industrialized core runtime with explicit lifecycle management."""

    def __init__(self, config: JarvisConfig | None = None) -> None:
        self.config = config or JarvisConfig.from_env()

        self.voice = None
        self.gesture = None
        self.llm = None
        self.gui = None
        self.device_controller = None
        self.personality = None
        self.threat_analyzer = None

        self.running = False
        self.processing_command = False
        self.responding = False
        self._threads: list[threading.Thread] = []

        self.command_handlers: dict[str, Callable[[str], str | None]] = {
            "llm": self._handle_llm,
            "device": self._handle_device,
            "gesture": self._handle_gesture,
            "threat": self._handle_threat,
            "personality": self._handle_personality,
        }

    def initialize(self) -> None:
        logger.info("Initializing modules")
        from modules.device_controller import DeviceController
        from modules.enhanced_gui import EnhancedGUI
        from modules.gesture_recognition import GestureRecognition
        from modules.llm_selector import LLMSelector
        from modules.personality import PersonalityModule
        from modules.threat_analyzer import ThreatAnalyzer
        from modules.voice_interface import VoiceInterface

        self.voice = VoiceInterface()
        self.gesture = GestureRecognition()
        self.llm = LLMSelector(
            openai_api_key=self.config.openai_api_key,
            huggingface_api_key=self.config.huggingface_api_key,
        )
        self.device_controller = DeviceController()
        self.personality = PersonalityModule()
        self.threat_analyzer = ThreatAnalyzer()
        self.device_controller.register_device("lights", interface="mock_interface")
        self.gui = EnhancedGUI()

    def process_command(self, command: str) -> str:
        if not command:
            return ""

        clean = command.strip()
        logger.info("Processing command: %s", clean)

        if clean.lower() in {"exit", "shutdown", "quit"}:
            self.shutdown()
            return "Shutting down..."

        if ":" in clean:
            prefix, payload = clean.split(":", maxsplit=1)
            handler = self.command_handlers.get(prefix.strip().lower())
            if handler:
                response = handler(payload.strip())
                return response or ""

        return (
            "I'm not sure how to help with that yet, sir. "
            "Would you like me to search the internet for information about it?"
        )

    def _handle_llm(self, payload: str) -> str:
        return self.llm.query_llm(payload) if self.llm else "LLM unavailable"

    def _handle_device(self, payload: str) -> str:
        return self.device_controller.process_command(payload) if self.device_controller else "Device controller unavailable"

    def _handle_threat(self, payload: str) -> str:
        return self.threat_analyzer.analyze_threat(payload) if self.threat_analyzer else "Threat analyzer unavailable"

    def _handle_personality(self, payload: str) -> str:
        return self.personality.process_interaction(payload) if self.personality else "Personality module unavailable"

    def _handle_gesture(self, payload: str) -> str:
        gesture_actions: dict[str, Callable[[], str]] = {
            "wave": self._toggle_voice_recognition,
            "thumbs_up": lambda: "Action confirmed",
            "thumbs_down": lambda: "Action cancelled",
            "point": lambda: "Option selected",
            "swipe_right": lambda: "Moving to next item",
            "swipe_left": lambda: "Moving to previous item",
            "fist": lambda: "Action stopped",
            "open_hand": lambda: "Action started",
        }
        action = gesture_actions.get(payload)
        return action() if action else f"Unrecognized gesture: {payload}"

    def _toggle_voice_recognition(self) -> str:
        if not self.voice:
            return "Voice interface unavailable"
        self.voice.enabled = not self.voice.enabled
        status = "enabled" if self.voice.enabled else "disabled"
        return f"Voice recognition {status}"

    def run_voice_loop(self) -> None:
        while self.running:
            if not self.processing_command and not self.responding and self.voice and self.gui:
                self.gui.set_listening_mode(True)
                self.gui.update_task("Listening", "Active")
                cmd = self.voice.listen()
                self.gui.set_listening_mode(False)

                if cmd:
                    self.gui.display_output(f"You said: {cmd}")
                    response = self.process_command(cmd)
                    if response:
                        self.gui.display_output(f"JARVIS: {response}")
            time.sleep(self.config.voice_poll_interval_seconds)

    def run_threat_monitor(self) -> None:
        while self.running:
            if not self.processing_command and self.threat_analyzer and self.gui and self.voice:
                threat_level = self.threat_analyzer.analyze()
                if threat_level >= 7:
                    alert = f"High threat detected! Level {threat_level}"
                    self.gui.update_task("Threat Alert", "High")
                    self.gui.display_output(f"JARVIS: {alert}")
                    self.voice.speak(alert)
            time.sleep(self.config.threat_poll_interval_seconds)

    def run_gesture_loop(self) -> None:
        if not self.gesture:
            return
        if not self.gesture.start():
            logger.warning("Gesture recognition failed to start")
            return

        while self.running:
            gesture = self.gesture.detect_gesture()
            if gesture != "none":
                response = self.process_command(f"gesture:{gesture}")
                logger.info("Gesture '%s' -> %s", gesture, response)
            time.sleep(self.config.gesture_poll_interval_seconds)

    def start(self) -> None:
        logger.info("Starting JARVIS runtime")
        self.running = True
        self.initialize()

        if self.gui:
            self.gui.start()
        time.sleep(1)

        self._threads = [
            threading.Thread(target=self.run_voice_loop, daemon=True),
            threading.Thread(target=self.run_threat_monitor, daemon=True),
            threading.Thread(target=self.run_gesture_loop, daemon=True),
        ]
        for thread in self._threads:
            thread.start()

        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self) -> None:
        logger.info("Shutdown initiated")
        self.running = False
        if self.gesture:
            self.gesture.release()
        if self.gui:
            self.gui.stop()
        logger.info("Shutdown complete")


if __name__ == "__main__":
    JarvisCore().start()
