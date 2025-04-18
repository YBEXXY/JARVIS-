import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎙️ Listening... Speak now.")
    audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("🧠 You said:", text)
    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand your voice.")
    except sr.RequestError as e:
        print("⚠️ Request error from Google:", e)
