"""Threat analyzer module."""

from __future__ import annotations

import random


class ThreatAnalyzer:
    def __init__(self) -> None:
        self.threat_level = 0
        self.anomaly_history: list[int] = []

    def analyze(self) -> int:
        self.threat_level = random.randint(0, 10)
        self.anomaly_history.append(self.threat_level)
        return self.threat_level

    def analyze_threat(self, _command: str | None = None) -> str:
        level = self.analyze()
        if level >= 7:
            return f"High threat detected! Level {level}"
        return f"Threat level normal: {level}"
