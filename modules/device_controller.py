"""Device control abstraction with explicit registration and command handling."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Device:
    name: str
    interface: str


class DeviceController:
    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    def register_device(self, name: str, interface: str) -> None:
        """Register a controllable device."""
        self.devices[name] = Device(name=name, interface=interface)
        logger.info("Registered device: %s (%s)", name, interface)

    def control_device(self, name: str, command: str) -> str:
        """Send an action command to a registered device."""
        device = self.devices.get(name)
        if not device:
            logger.warning("Attempted control on unknown device: %s", name)
            return f"Device '{name}' is not registered."

        logger.info("Dispatching command '%s' to %s", command, name)
        return f"Command '{command}' sent to {name}."

    def process_command(self, command: str) -> str:
        """Process command format '<device> <action>'."""
        if not command:
            return "No device command provided."

        parts = command.strip().split(maxsplit=1)
        if len(parts) < 2:
            return "Please provide a device name and an action, e.g. 'lights on'."

        device_name, action = parts[0], parts[1]
        return self.control_device(device_name, action)
