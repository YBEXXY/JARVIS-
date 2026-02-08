from modules.device_controller import DeviceController


def test_device_register_and_control():
    controller = DeviceController()
    controller.register_device("lamp", "mock")

    result = controller.process_command("lamp on")
    assert result == "Command 'on' sent to lamp."


def test_device_unknown():
    controller = DeviceController()
    result = controller.process_command("tv on")
    assert result == "Device 'tv' is not registered."
