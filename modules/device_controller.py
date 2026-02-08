class DeviceController:
    def __init__(self):
        # Initialize communication protocols, devices, etc.
        self.devices = {}  # Placeholder for device registry

    def register_device(self, name, interface):
        """Register a new device with its control interface."""
        self.devices[name] = interface
        print(f"[Device] Registered device: {name}")

    def control_device(self, name, command):
        """Send a command to a device."""
        if name in self.devices:
            print(f"[Device] Command '{command}' sent to {name}")
            # In a real scenario, interface with device API or protocol.
            return f"Command '{command}' sent to {name}."
        else:
            print(f"[Device] Device {name} not registered.")
            return f"Device '{name}' is not registered."

    def process_command(self, command):
        """Process device commands in the format '<device> <action>'."""
        if not command:
            return "No device command provided."

        parts = command.strip().split(maxsplit=1)
        if len(parts) < 2:
            return "Please provide a device name and an action, e.g. 'lights on'."

        device_name, action = parts[0], parts[1]
        return self.control_device(device_name, action)
