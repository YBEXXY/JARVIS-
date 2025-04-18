# JARVIS ASSISTANT - USER MANUAL

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Voice Commands](#voice-commands)
5. [Gesture Recognition](#gesture-recognition)
6. [GUI Features](#gui-features)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Customization](#customization)
10. [FAQ](#faq)

## Introduction

JARVIS (Just A Rather Very Intelligent System) is an AI assistant that combines voice recognition, gesture control, and a modern graphical interface. This manual will guide you through installing, setting up, and using JARVIS effectively.

### Key Features
- **Voice Control**: Natural language processing for voice commands
- **Gesture Recognition**: Hand gesture detection for alternative control
- **Enhanced GUI**: Modern interface with visual feedback
- **Device Control**: Control smart devices and systems
- **Threat Analysis**: Security monitoring and alerts
- **Personality Module**: Natural conversation capabilities
- **LLM Integration**: Advanced language model queries

## Installation

### System Requirements
- Windows 10 or later
- Python 3.8 or later
- Webcam for gesture recognition
- Microphone for voice commands
- Speakers for audio output

### Installation Steps

1. **Download the JARVIS Assistant**
   - Download the latest release from the GitHub repository
   - Extract the files to a location of your choice

2. **Install Python Dependencies**
   - Open a command prompt or terminal
   - Navigate to the JARVIS directory
   - Run the following command:
     ```
     pip install -r requirements.txt
     ```

3. **Configure Environment Variables**
   - Open the `.env` file in a text editor
   - Add your API keys for services like OpenWeather:
     ```
     OPENWEATHER_API_KEY=your_api_key_here
     ```
   - Save the file

## Getting Started

### Starting JARVIS

1. Open a command prompt or terminal
2. Navigate to the JARVIS directory
3. Run the following command:
   ```
   python jarvis_main.py
   ```
4. JARVIS will initialize and display the GUI
5. You'll hear a startup message: "JARVIS online. Security protocol active. Awaiting authorization."

### Security Activation

JARVIS requires a security keyword to activate:

1. Say "WAKE UP JARVIS" clearly
2. JARVIS will respond with a security clearance message
3. After activation, you can use JARVIS normally

### Basic Interaction

1. After activation, say "Hey JARVIS" or "Hello JARVIS"
2. JARVIS will respond and be ready for your commands
3. Speak your command clearly
4. JARVIS will process your command and respond

## Voice Commands

JARVIS understands a variety of voice commands:

### General Commands
- "Hey JARVIS" or "Hello JARVIS" - Activate JARVIS
- "What time is it?" - Get the current time
- "What's the date today?" - Get today's date
- "How are you?" - Get a status response
- "Thank you" - Receive a thank you response
- "Goodbye" or "Exit" - End the session

### Web Commands
- "Open YouTube" - Opens YouTube in your default browser
- "Open Google" - Opens Google in your default browser
- "Search for [topic]" - Searches Google for the specified topic

### System Commands
- "System status" or "System info" - Get system resource usage
- "Weather in [city]" - Get weather information for a city

### Conversation
- JARVIS can engage in basic conversation
- Try asking "How are you?" or "What can you do?"

## Gesture Recognition

JARVIS can recognize hand gestures for alternative control:

### Available Gestures
- **👋 Wave** - Toggle voice recognition on/off
- **👍 Thumbs Up** - Confirm/Accept actions
- **👎 Thumbs Down** - Cancel/Reject actions
- **👆 Point** - Select/Choose options
- **👉 Swipe Right** - Move to next item
- **👈 Swipe Left** - Move to previous item
- **✊ Fist** - Stop/Pause actions
- **✋ Open Hand** - Start/Resume actions

### Using Gesture Recognition

1. When JARVIS is running, a window titled "Gesture Recognition" will open
2. Position your hand in front of the camera
3. Make the desired gesture
4. JARVIS will detect the gesture and perform the corresponding action

### Gesture Tips
- Ensure good lighting for better gesture detection
- Position your hand about 1-2 feet from the camera
- Make clear, deliberate gestures
- If a gesture isn't detected, try adjusting your hand position or lighting

## GUI Features

JARVIS has a modern graphical interface with several features:

### Main Interface
- **Central Sphere**: Changes color based on JARVIS's state
  - Blue: Idle/Ready
  - Red: Listening
  - Green: Processing
- **Status Display**: Shows current task and status
- **Command History**: Displays recent commands and responses
- **Audio Visualization**: Shows audio levels when speaking

### Interaction Methods
- **Voice**: Speak commands to JARVIS
- **Text Input**: Type commands in the text field and press Enter
- **Gestures**: Use hand gestures for control

## Advanced Features

### Device Control
JARVIS can control smart devices:

1. Register a device:
   ```
   "Register device [name]"
   ```

2. Control a device:
   ```
   "Control [device] [action]"
   ```

### Threat Analysis
JARVIS can analyze system security:

1. Request a threat analysis:
   ```
   "Analyze security" or "Check for threats"
   ```

2. JARVIS will report any detected threats

### LLM Queries
JARVIS can answer questions using language models:

1. Ask a question:
   ```
   "What is [topic]?" or "Tell me about [subject]"
   ```

2. JARVIS will query the language model and provide an answer

## Troubleshooting

### Voice Recognition Issues
- **Problem**: JARVIS doesn't recognize your voice commands
  - **Solution**: Check your microphone settings and ensure it's properly connected
  - **Solution**: Speak clearly and in a quiet environment
  - **Solution**: Try adjusting the microphone sensitivity in your system settings

### Gesture Recognition Problems
- **Problem**: JARVIS doesn't detect your gestures
  - **Solution**: Check your camera connection and ensure it's properly connected
  - **Solution**: Ensure good lighting in the room
  - **Solution**: Make clear, deliberate gestures
  - **Solution**: Position your hand about 1-2 feet from the camera

### GUI Display Issues
- **Problem**: The GUI doesn't display properly
  - **Solution**: Check your screen resolution and ensure it's compatible
  - **Solution**: Update your graphics drivers
  - **Solution**: Restart JARVIS

### General Issues
- **Problem**: JARVIS crashes or freezes
  - **Solution**: Check the console for error messages
  - **Solution**: Ensure all dependencies are installed correctly
  - **Solution**: Restart JARVIS

## Customization

### Voice Settings
You can customize JARVIS's voice:

1. Open the `modules/voice_interface.py` file
2. Modify the voice settings:
   ```python
   self.engine.setProperty('rate', 150)  # Speed of speech
   self.engine.setProperty('volume', 1.0)  # Volume
   ```

### Gesture Actions
You can customize the actions for each gesture:

1. Open the `custom_gesture_test.py` file
2. Modify the `ACTION_FUNCTIONS` dictionary to change the actions

### Adding New Commands
You can add new commands to JARVIS:

1. Open the `jarvis_commands.py` file
2. Add a new condition in the `execute_command` function:
   ```python
   elif "your command" in command:
       return "Your response"
   ```

## FAQ

### Q: How do I activate JARVIS?
A: Say "WAKE UP JARVIS" to activate the security protocol, then say "Hey JARVIS" to start interacting.

### Q: Can I use JARVIS without a microphone?
A: Yes, you can use the text input field in the GUI to type commands.

### Q: Can I use JARVIS without a camera?
A: Yes, but you won't be able to use gesture recognition features.

### Q: How do I stop JARVIS?
A: Say "Exit" or "Shutdown" or press Ctrl+C in the terminal.

### Q: Can I customize JARVIS's voice?
A: Yes, you can modify the voice settings in the voice_interface.py file.

### Q: How do I add new commands to JARVIS?
A: You can add new commands by modifying the jarvis_commands.py file.

---

Thank you for using JARVIS Assistant! For more information, visit our GitHub repository or contact support. 