from jarvis_core import JarvisCore


class StubLLM:
    def query_llm(self, payload):
        return f"LLM:{payload}"


class StubDevice:
    def process_command(self, payload):
        return f"DEVICE:{payload}"


class StubThreat:
    def analyze_threat(self, payload):
        return f"THREAT:{payload}"


class StubPersonality:
    def process_interaction(self, payload):
        return f"PERSONALITY:{payload}"


class StubVoice:
    enabled = True


def test_command_routing_prefix_handlers():
    core = JarvisCore()
    core.llm = StubLLM()
    core.device_controller = StubDevice()
    core.threat_analyzer = StubThreat()
    core.personality = StubPersonality()
    core.voice = StubVoice()

    assert core.process_command("llm:hello") == "LLM:hello"
    assert core.process_command("device:lights on") == "DEVICE:lights on"
    assert core.process_command("threat:scan") == "THREAT:scan"
    assert core.process_command("personality:hi") == "PERSONALITY:hi"
    assert core.process_command("gesture:wave") == "Voice recognition disabled"


def test_command_shutdown_path():
    core = JarvisCore()
    core.running = True
    assert core.process_command("shutdown") == "Shutting down..."
    assert core.running is False
