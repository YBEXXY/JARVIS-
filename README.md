# JARVIS Assistant

A modern, voice-controlled AI assistant with an enhanced graphical interface and multiple interaction modes.

## Features

- **Voice Control**: Natural language processing for voice commands
- **Gesture Recognition**: Hand gesture detection for alternative control
- **Enhanced GUI**: Modern interface with visual feedback
- **Device Control**: Control smart devices and systems
- **Threat Analysis**: Security monitoring and alerts
- **Personality Module**: Natural conversation capabilities
- **LLM Integration**: Advanced language model queries

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jarvis-assistant.git
cd jarvis-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start JARVIS:
```bash
python jarvis_core.py
```

2. Voice Commands:
   - "Hey JARVIS" or "JARVIS" to activate
   - "What is [topic]?" for information queries
   - "Control [device] [action]" for device control
   - "Detect gesture" for gesture recognition
   - "Analyze security" for threat analysis
   - "Exit" or "Shutdown" to close

3. Gesture Controls:
   - Wave hand to activate
   - Thumbs up/down for yes/no
   - Point for selection
   - Swipe for navigation

4. GUI Features:
   - Sphere changes color based on state:
     - Blue: Idle/Ready
     - Red: Listening
     - Green: Processing
   - Task status display
   - Audio level visualization
   - Command history

## Module Overview

1. **Voice Interface** (`modules/voice_interface.py`):
   - Speech recognition
   - Text-to-speech output
   - Voice command processing

2. **Gesture Recognition** (`modules/gesture_recognition.py`):
   - Hand tracking
   - Gesture classification
   - Motion detection

3. **Enhanced GUI** (`modules/enhanced_gui.py`):
   - Modern interface
   - Visual feedback
   - Status display
   - Audio visualization

4. **Device Controller** (`modules/device_controller.py`):
   - Smart device management
   - Command routing
   - Status monitoring

5. **Personality Module** (`modules/personality.py`):
   - Natural conversation
   - Response generation
   - Context awareness

6. **Threat Analyzer** (`modules/threat_analyzer.py`):
   - Security monitoring
   - Threat detection
   - Alert system

7. **LLM Selector** (`modules/llm_selector.py`):
   - Language model integration
   - Query processing
   - Response generation

## Configuration

1. Voice Settings:
   - Adjust microphone sensitivity
   - Change voice recognition language
   - Modify speech rate

2. GUI Settings:
   - Customize colors
   - Adjust animation speed
   - Change layout

3. Device Settings:
   - Add new devices
   - Configure interfaces
   - Set default actions

## Troubleshooting

1. Voice Recognition Issues:
   - Check microphone settings
   - Ensure proper language pack installation
   - Verify audio drivers

2. Gesture Recognition Problems:
   - Check camera connection
   - Adjust lighting conditions
   - Calibrate gesture sensitivity

3. GUI Display Issues:
   - Update graphics drivers
   - Check screen resolution
   - Verify Python GUI dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 