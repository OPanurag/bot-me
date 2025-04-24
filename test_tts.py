"""This script tests the text-to-speech functionality of pyttsx3.
This can be used to ensure that the TTS system works correctly before integrating (Debugging)."""
import pyttsx3

def test_pyttsx3():
    try:
        engine = pyttsx3.init()
        engine.say("This is a test of the text to speech functionality")
        engine.runAndWait()
        print("pyttsx3 test completed successfully")
    except Exception as e:
        print(f"Error with pyttsx3: {e}")

if __name__ == "__main__":
    test_pyttsx3()