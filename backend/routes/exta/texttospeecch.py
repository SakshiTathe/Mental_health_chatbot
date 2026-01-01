import pyttsx3

def text_to_speech(text, voice_gender='female', rate=180):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voice_gender.lower() == 'male':
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()
#text_to_speech("Mujhe bahut stress lag raha hai today", voice_gender='female')

import speech_recognition as sr

def speech_to_text(timeout=5, phrase_time_limit=10):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(" Speak now...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            print(" You said:", text)
            return text
        except sr.WaitTimeoutError:
            print(" Listening timed out. Try again.")
            return ""
        except sr.UnknownValueError:
            print(" Sorry, could not understand the audio.")
            return ""
        except sr.RequestError:
            print(" Could not reach speech recognition service.")
            return ""
spoken_text = speech_to_text()
text_to_speech(f"You said: {spoken_text}")

from gtts import gTTS
import os

def hinglish_tts(text, lang='hi'):
    tts = gTTS(text=text, lang=lang, slow=False, tld='co.in')
    tts.save("output.mp3")
    os.system("start output.mp3")

#hinglish_tts("Hello there, how are you feeling today?")
