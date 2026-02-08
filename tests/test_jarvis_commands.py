from jarvis_commands import execute_command


def test_blank_command():
    assert execute_command("  ") == "Please tell me what you'd like me to do."


def test_time_command_contains_phrase():
    assert "The current time is" in execute_command("time")
