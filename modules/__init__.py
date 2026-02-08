"""Core modules package for JARVIS.

This package intentionally avoids eager submodule imports so constrained
or partially provisioned environments can still import lightweight modules.
"""

__all__ = [
    "DeviceController",
    "EnhancedGUI",
    "GestureRecognition",
    "GUIHandler",
    "LLMSelector",
    "PersonalityModule",
    "ThreatAnalyzer",
    "VoiceInterface",
]
